from __future__ import annotations

import math
import os
import random
import time
from pathlib import Path
from typing import Any

import torch
from torch import nn
from torch.nn import functional as F

from .common import CRASH_EXIT_CODE, GENESIS_HASH, ROOT, SCHEMA_VERSION, RunLogger, append_jsonl, configure_determinism, hash_file, read_json, read_jsonl, sha256_json, tensor_state_hash, write_json, write_jsonl
from .data import ByteTokenizer
from .interfaces import CheckpointStoreProtocol, LedgerStoreProtocol
from .model import TinyCausalLM, make_model, state_dict_cpu

def load_batch(artifact_root: Path, batch_index: int) -> dict[str, Any]:
    return read_json(artifact_root / "batches" / f"batch_{batch_index:04d}.json")


def batch_tensors(batch: dict[str, Any]) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    return (
        torch.tensor([sequence["input_ids"] for sequence in batch["sequences"]], dtype=torch.long),
        torch.tensor([sequence["labels"] for sequence in batch["sequences"]], dtype=torch.long),
        torch.tensor([sequence["loss_mask"] for sequence in batch["sequences"]], dtype=torch.float32),
        torch.tensor([sequence["position_ids"] for sequence in batch["sequences"]], dtype=torch.long),
        torch.tensor([sequence["attention_mask"] for sequence in batch["sequences"]], dtype=torch.bool),
    )


def ledger_head(records: list[dict[str, Any]]) -> str:
    return records[-1]["record_hash"] if records else GENESIS_HASH


def verify_hash_chain(records: list[dict[str, Any]], starting_hash: str = GENESIS_HASH) -> tuple[bool, str]:
    previous = starting_hash
    for record in records:
        if record.get("previous_hash") != previous:
            return False, previous
        core = {key: value for key, value in record.items() if key != "record_hash"}
        expected = sha256_json(core)
        if record.get("record_hash") != expected:
            return False, previous
        previous = expected
    return True, previous


class JsonlHashChainLedger(LedgerStoreProtocol):
    """Append-only local ledger backend with canonical SHA-256 chaining."""

    def __init__(self, path: Path, starting_hash: str = GENESIS_HASH):
        self.path = path
        self.starting_hash = starting_hash

    def read(self) -> list[dict[str, Any]]:
        return read_jsonl(self.path)

    def verify(self) -> tuple[bool, str]:
        return verify_hash_chain(self.read(), self.starting_hash)

    @property
    def head(self) -> str:
        return self.verify()[1]

    def append(self, record: dict[str, Any]) -> None:
        valid, current_head = self.verify()
        if not valid:
            raise ValueError("cannot append to an invalid ledger")
        if record.get("previous_hash") != current_head:
            raise ValueError("record does not extend the current ledger head")
        append_jsonl(self.path, record)


class LocalCheckpointStore(CheckpointStoreProtocol):
    """Atomic local checkpoint backend; replaceable by an object-store adapter."""

    def __init__(self, artifact_root: Path):
        self.directory = artifact_root / "checkpoints"

    def save(self, name: str, state: dict[str, Any]) -> Path:
        self.directory.mkdir(parents=True, exist_ok=True)
        final_path = self.directory / f"{name}.pt"
        temporary = final_path.with_suffix(".pt.tmp")
        torch.save(state, temporary)
        os.replace(temporary, final_path)
        return final_path

    def load(self, checkpoint: Path) -> dict[str, Any]:
        return torch.load(checkpoint, map_location="cpu", weights_only=False)


def source_for_position(sequence: dict[str, Any], packed_position: int) -> dict[str, Any]:
    for ref in sequence["source_spans"]:
        if ref["packed_start"] <= packed_position < ref["packed_end"]:
            relative = packed_position - ref["packed_start"] - 1
            token_offset = ref["token_start"] + max(0, min(relative, ref["token_end"] - ref["token_start"]))
            return {**ref, "source_token_offset": token_offset}
    return {"doc_id": None, "source_token_offset": None}


def optimizer_and_scheduler(model: nn.Module, config: dict[str, Any]) -> tuple[torch.optim.Optimizer, torch.optim.lr_scheduler.LRScheduler]:
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config["model"]["learning_rate"],
        weight_decay=config["model"]["weight_decay"],
    )
    total_steps = len(config["stages"]) * config["steps_per_stage"]
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lambda step: max(0.5, 1.0 - 0.5 * step / total_steps))
    return optimizer, scheduler


def save_checkpoint(
    artifact_root: Path,
    name: str,
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.lr_scheduler.LRScheduler,
    next_batch_index: int,
    config_hash: str,
    tokenizer_hash: str,
    manifest_hash: str,
    run_id: str,
    logger: RunLogger | None = None,
    parent: dict[str, Any] | None = None,
) -> Path:
    ledger = JsonlHashChainLedger(artifact_root / "ledgers" / "step_ledger.jsonl")
    records = ledger.read()
    chain_ok, head = ledger.verify()
    if not chain_ok:
        raise ValueError("cannot checkpoint an invalid ledger chain")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "model_state": state_dict_cpu(model),
        "optimizer_state": optimizer.state_dict(),
        "scheduler_state": scheduler.state_dict(),
        "python_rng_state": random.getstate(),
        "torch_rng_state": torch.get_rng_state(),
        "next_batch_index": next_batch_index,
        "ledger_record_count": len(records),
        "ledger_head_hash": head,
        "config_hash": config_hash,
        "tokenizer_hash": tokenizer_hash,
        "manifest_hash": manifest_hash,
        "model_state_hash": tensor_state_hash(state_dict_cpu(model)),
        "parent": parent,
    }
    final_path = LocalCheckpointStore(artifact_root).save(name, payload)
    metadata = {
        key: value
        for key, value in payload.items()
        if key not in {"model_state", "optimizer_state", "scheduler_state", "python_rng_state", "torch_rng_state"}
    }
    metadata["checkpoint_file"] = str(final_path.relative_to(artifact_root))
    metadata["checkpoint_file_hash"] = hash_file(final_path)
    write_json(final_path.with_suffix(".json"), metadata)
    if logger:
        logger.log("checkpoint saved", f"{name}; next_batch={next_batch_index}; ledger_offset={len(records)}")
        logger.log("checkpoint_saved", f"{name}", "PASS")
    return final_path


def load_checkpoint(
    checkpoint_path: Path,
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.lr_scheduler.LRScheduler,
) -> dict[str, Any]:
    payload = LocalCheckpointStore(checkpoint_path.parents[1]).load(checkpoint_path)
    model.load_state_dict(payload["model_state"])
    optimizer.load_state_dict(payload["optimizer_state"])
    scheduler.load_state_dict(payload["scheduler_state"])
    random.setstate(payload["python_rng_state"])
    torch.set_rng_state(payload["torch_rng_state"])
    if tensor_state_hash(state_dict_cpu(model)) != payload["model_state_hash"]:
        raise ValueError("checkpoint model state hash mismatch")
    return payload


def train_batch(
    model: TinyCausalLM,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.lr_scheduler.LRScheduler,
    batch: dict[str, Any],
    config: dict[str, Any],
    previous_hash: str,
    run_id: str,
) -> dict[str, Any]:
    for sequence in batch["sequences"]:
        if any(ref["shard_id"].startswith(("eval-", "validation-", "selection_proxy-")) for ref in sequence["source_spans"]):
            raise PermissionError("trainer firewall blocked a non-training source")
    inputs, labels, mask, positions, attention = batch_tensors(batch)
    useful_total = int(mask.sum().item())
    if useful_total <= 0:
        raise ValueError("batch has no loss-bearing tokens")
    optimizer.zero_grad(set_to_none=True)
    pre_model_hash = tensor_state_hash(state_dict_cpu(model))
    per_token_losses = torch.zeros_like(mask)
    microbatch_size = config["microbatch_size"]
    started = time.perf_counter()
    for start in range(0, inputs.shape[0], microbatch_size):
        end = start + microbatch_size
        logits = model(inputs[start:end], positions[start:end], attention[start:end])
        losses = F.cross_entropy(
            logits.reshape(-1, logits.shape[-1]), labels[start:end].reshape(-1), reduction="none"
        ).reshape_as(mask[start:end])
        per_token_losses[start:end] = losses.detach()
        ((losses * mask[start:end]).sum() / useful_total).backward()
    gradient_norm = float(torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=10.0).item())
    learning_rate = float(optimizer.param_groups[0]["lr"])
    optimizer.step()
    scheduler.step()
    elapsed = time.perf_counter() - started
    post_model_hash = tensor_state_hash(state_dict_cpu(model))
    sample_losses: list[float] = []
    token_traces: list[dict[str, Any]] = []
    for sequence_index, sequence in enumerate(batch["sequences"]):
        sequence_mask = mask[sequence_index].bool()
        values = per_token_losses[sequence_index][sequence_mask]
        sample_losses.append(float(values.mean().item()))
        for query_position in torch.nonzero(sequence_mask, as_tuple=False).flatten().tolist():
            target_position = query_position + 1
            source = source_for_position(sequence, target_position)
            token_traces.append(
                {
                    "sequence_index": sequence_index,
                    "query_position": query_position,
                    "target_position": target_position,
                    "target_token_id": sequence["labels"][query_position],
                    "target_role": sequence["token_roles"][target_position],
                    "loss": float(per_token_losses[sequence_index, query_position].item()),
                    "doc_id": source.get("doc_id"),
                    "shard_id": source.get("shard_id"),
                    "row_id": source.get("row_id"),
                    "source_token_offset": source.get("source_token_offset"),
                }
            )
    mean_loss = sum(trace["loss"] for trace in token_traces) / len(token_traces)
    consumption = {
        "batch_id": batch["batch_id"],
        "batch_index": batch["batch_index"],
        "stage": batch["stage"],
        "lane_counts": batch["lane_counts"],
        "tensor_hash": batch["tensor_hash"],
        "sequence_hashes": batch["sequence_hashes"],
        "source_spans": [span for sequence in batch["sequences"] for span in sequence["source_spans"]],
        "opus_decision_ids": sorted({decision for sequence in batch["sequences"] for decision in sequence["opus_decision_ids"]}),
        "raw_tokens": batch["raw_tokens"],
        "non_pad_tokens": batch["non_pad_tokens"],
        "loss_bearing_tokens": batch["loss_bearing_tokens"],
    }
    learning = {
        "mean_loss": mean_loss,
        "perplexity": math.exp(min(mean_loss, 20.0)),
        "sample_losses": sample_losses,
        "token_losses": token_traces,
        "gradient_norm": gradient_norm,
        "learning_rate": learning_rate,
        "elapsed_seconds": elapsed,
        "pre_model_state_hash": pre_model_hash,
        "post_model_state_hash": post_model_hash,
    }
    core = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "global_step": batch["batch_index"],
        "previous_hash": previous_hash,
        "consumption": consumption,
        "learning": learning,
    }
    return {**core, "record_hash": sha256_json(core)}


def write_ledger_projections(artifact_root: Path) -> None:
    records = JsonlHashChainLedger(artifact_root / "ledgers" / "step_ledger.jsonl").read()
    consumption = [
        {
            "schema_version": SCHEMA_VERSION,
            "run_id": record["run_id"],
            "global_step": record["global_step"],
            "step_record_hash": record["record_hash"],
            **record["consumption"],
        }
        for record in records
    ]
    learning = [
        {
            "schema_version": SCHEMA_VERSION,
            "run_id": record["run_id"],
            "global_step": record["global_step"],
            "step_record_hash": record["record_hash"],
            "batch_id": record["consumption"]["batch_id"],
            **record["learning"],
        }
        for record in records
    ]
    write_jsonl(artifact_root / "ledgers" / "consumption.jsonl", consumption)
    write_jsonl(artifact_root / "ledgers" / "learning.jsonl", learning)


def training_worker(artifact_root: Path, mode: str) -> int:
    config = read_json(ROOT / "config" / "demo.json")
    tokenizer = ByteTokenizer(read_json(ROOT / "config" / "tokenizer.json"))
    configure_determinism(config["seed"])
    logger = RunLogger(artifact_root / "run.log")
    model = make_model(config, tokenizer)
    optimizer, scheduler = optimizer_and_scheduler(model, config)
    checkpoint_name = "checkpoint_genesis.pt" if mode == "crash" else f"checkpoint_step_{config['crash_after_step']:04d}.pt"
    checkpoint_path = artifact_root / "checkpoints" / checkpoint_name
    payload = load_checkpoint(checkpoint_path, model, optimizer, scheduler)
    ledger = JsonlHashChainLedger(artifact_root / "ledgers" / "step_ledger.jsonl")
    records = ledger.read()
    chain_ok, head = ledger.verify()
    if not chain_ok or len(records) != payload["ledger_record_count"] or head != payload["ledger_head_hash"]:
        raise ValueError("checkpoint and ledger boundary disagree")
    start_index = payload["next_batch_index"]
    total_steps = len(config["stages"]) * config["steps_per_stage"]
    if mode == "resume":
        intent = read_json(artifact_root / "checkpoints" / "crash_intent.json")
        next_batch = load_batch(artifact_root, start_index)
        if next_batch["batch_id"] != intent["expected_batch_id"] or next_batch["tensor_hash"] != intent["expected_tensor_hash"]:
            raise ValueError("resumed batch does not match crash intent")
        logger.log("run resumed", f"checkpoint={checkpoint_name}; next={next_batch['batch_id']}")
        logger.log("resume_next_batch_matched", next_batch["batch_id"], "PASS")
    stop_index = config["crash_after_step"] if mode == "crash" else total_steps
    for batch_index in range(start_index, stop_index):
        batch = load_batch(artifact_root, batch_index)
        record = train_batch(model, optimizer, scheduler, batch, config, head, payload["run_id"])
        ledger.append(record)
        head = record["record_hash"]
        logger.log("training batch committed", f"step={batch_index}; batch={batch['batch_id']}; loss={record['learning']['mean_loss']:.6f}")
    manifest_hash = read_json(artifact_root / "manifests" / "shard_index.json")["index_hash"]
    config_hash = sha256_json(config)
    if mode == "crash":
        saved = save_checkpoint(
            artifact_root,
            f"checkpoint_step_{stop_index:04d}",
            model,
            optimizer,
            scheduler,
            stop_index,
            config_hash,
            tokenizer.tokenizer_hash,
            manifest_hash,
            payload["run_id"],
            logger,
        )
        expected = load_batch(artifact_root, stop_index)
        intent = {
            "schema_version": SCHEMA_VERSION,
            "checkpoint": str(saved.relative_to(artifact_root)),
            "expected_batch_index": stop_index,
            "expected_batch_id": expected["batch_id"],
            "expected_tensor_hash": expected["tensor_hash"],
            "expected_source_span_hash": sha256_json([sequence["source_spans"] for sequence in expected["sequences"]]),
        }
        write_json(artifact_root / "checkpoints" / "crash_intent.json", intent)
        logger.log("crash simulated", f"exit_code={CRASH_EXIT_CODE}; expected_next={expected['batch_id']}")
        os._exit(CRASH_EXIT_CODE)
    save_checkpoint(
        artifact_root,
        f"checkpoint_step_{total_steps:04d}",
        model,
        optimizer,
        scheduler,
        total_steps,
        config_hash,
        tokenizer.tokenizer_hash,
        manifest_hash,
        payload["run_id"],
        logger,
    )
    write_ledger_projections(artifact_root)
    return 0

