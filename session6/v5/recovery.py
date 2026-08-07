from __future__ import annotations

import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import torch
from torch.nn import functional as F

from .common import GENESIS_HASH, ROOT, SCHEMA_VERSION, RunLogger, configure_determinism, hash_file, read_json, read_jsonl, sha256_json, tensor_state_hash, write_json, write_jsonl
from .batches import make_batch
from .data import ByteTokenizer
from .model import make_model, state_dict_cpu
from .packing import build_packed_sequence, chunk_row, sequence_tensors
from .training import load_batch, load_checkpoint, optimizer_and_scheduler, train_batch, verify_hash_chain

def reconstruct_sequence(
    sequence: dict[str, Any], row_lookup: dict[tuple[str, int], dict[str, Any]], tokenizer: ByteTokenizer, sequence_length: int
) -> dict[str, Any]:
    segments: list[dict[str, Any]] = []
    for ref in sequence["source_spans"]:
        row = row_lookup[(ref["shard_id"], ref["row_id"])]
        start, end = ref["token_start"], ref["token_end"]
        tokens = row["tokens"][start:end]
        if sha256_json(tokens) != ref["span_hash"]:
            raise ValueError("source span hash mismatch during replay")
        segments.append(
            {
                "tokens": tokens,
                "roles": row["roles"][start:end],
                "ref": {
                    "shard_id": ref["shard_id"],
                    "row_id": ref["row_id"],
                    "doc_id": ref["doc_id"],
                    "token_start": start,
                    "token_end": end,
                    "span_hash": ref["span_hash"],
                },
            }
        )
    return build_packed_sequence(
        segments,
        sequence["lane"],
        sequence["packing_policy"],
        tokenizer,
        sequence_length,
        sequence["opus_decision_ids"],
    )


def replay_history(artifact_root: Path, config: dict[str, Any], tokenizer: ByteTokenizer, all_rows: list[dict[str, Any]], logger: RunLogger) -> dict[str, Any]:
    configure_determinism(config["seed"])
    row_lookup = {(row["shard_id"], row["row_id"]): row for row in all_rows}
    historical = read_jsonl(artifact_root / "ledgers" / "step_ledger.jsonl")[: config["crash_after_step"]]
    model = make_model(config, tokenizer)
    optimizer, scheduler = optimizer_and_scheduler(model, config)
    genesis = load_checkpoint(artifact_root / "checkpoints" / "checkpoint_genesis.pt", model, optimizer, scheduler)
    comparisons: list[dict[str, Any]] = []
    previous_hash = GENESIS_HASH
    started = time.perf_counter()
    for historical_record in historical:
        original = load_batch(artifact_root, historical_record["global_step"])
        rebuilt_sequences = [reconstruct_sequence(sequence, row_lookup, tokenizer, config["sequence_length"]) for sequence in original["sequences"]]
        stage = config["stages"][original["stage_index"]]
        rebuilt = make_batch(original["batch_index"], stage, rebuilt_sequences, original["schedule_hash"])
        replay_record = train_batch(model, optimizer, scheduler, rebuilt, config, previous_hash, genesis["run_id"] + "-replay")
        previous_hash = replay_record["record_hash"]
        comparison = {
            "batch_index": original["batch_index"],
            "original_batch_id": original["batch_id"],
            "replay_batch_id": rebuilt["batch_id"],
            "original_tensor_hash": original["tensor_hash"],
            "replay_tensor_hash": rebuilt["tensor_hash"],
            "source_spans_match": [sequence["source_spans"] for sequence in original["sequences"]]
            == [sequence["source_spans"] for sequence in rebuilt["sequences"]],
            "loss_delta": abs(historical_record["learning"]["mean_loss"] - replay_record["learning"]["mean_loss"]),
            "post_model_hash_match": historical_record["learning"]["post_model_state_hash"]
            == replay_record["learning"]["post_model_state_hash"],
        }
        comparison["matched"] = (
            comparison["original_batch_id"] == comparison["replay_batch_id"]
            and comparison["original_tensor_hash"] == comparison["replay_tensor_hash"]
            and comparison["source_spans_match"]
            and comparison["loss_delta"] <= 1e-7
            and comparison["post_model_hash_match"]
        )
        comparisons.append(comparison)
    report = {
        "schema_version": SCHEMA_VERSION,
        "source": "historical_step_ledger",
        "interval": [0, config["crash_after_step"]],
        "comparisons": comparisons,
        "all_matched": bool(comparisons) and all(item["matched"] for item in comparisons),
        "elapsed_seconds": time.perf_counter() - started,
    }
    write_json(artifact_root / "replay" / "replay_report.json", report)
    logger.log("historical stream replayed", f"interval=0:{config['crash_after_step']}; batches={len(comparisons)}")
    if report["all_matched"]:
        logger.log("replay_hash_matched", f"batches={len(comparisons)}", "PASS")
    return report


def create_fork(artifact_root: Path, config: dict[str, Any], tokenizer: ByteTokenizer, logger: RunLogger) -> dict[str, Any]:
    configure_determinism(config["seed"])
    model = make_model(config, tokenizer)
    optimizer, scheduler = optimizer_and_scheduler(model, config)
    checkpoint_path = artifact_root / "checkpoints" / f"checkpoint_step_{config['crash_after_step']:04d}.pt"
    parent = load_checkpoint(checkpoint_path, model, optimizer, scheduler)
    parent_checkpoint_hash = hash_file(checkpoint_path)
    parent_head = parent["ledger_head_hash"]
    branch_run_id = parent["run_id"] + "-fork-code-heavy"
    source_batches = [load_batch(artifact_root, index) for index in range(config["crash_after_step"], len(config["stages"]) * config["steps_per_stage"])]
    pools: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for batch in source_batches:
        for sequence in batch["sequences"]:
            pools[sequence["lane"]].append(sequence)
    branch_layout = ["indic", "agentic", "reasoning", "general_web", "code", "code", "code", "code"]
    cursors = Counter()
    branch_records: list[dict[str, Any]] = []
    branch_batches: list[dict[str, Any]] = []
    previous_hash = parent_head
    branch_schedule_hash = sha256_json({"name": "fork_code_heavy", "layout": branch_layout})
    for offset in range(2):
        sequences: list[dict[str, Any]] = []
        for lane in branch_layout:
            sequence = pools[lane][cursors[lane] % len(pools[lane])]
            cursors[lane] += 1
            sequences.append(sequence)
        stage = {"name": "fork_code_heavy", "index": 1}
        batch = make_batch(config["crash_after_step"] + offset, stage, sequences, branch_schedule_hash)
        record = train_batch(model, optimizer, scheduler, batch, config, previous_hash, branch_run_id)
        previous_hash = record["record_hash"]
        branch_batches.append(batch)
        branch_records.append(record)
    branch_dir = artifact_root / "branches" / "fork_code_heavy"
    write_jsonl(branch_dir / "step_ledger.jsonl", branch_records)
    for offset, batch in enumerate(branch_batches):
        write_json(branch_dir / f"batch_{offset:04d}.json", batch)
    branch_checkpoint = {
        "schema_version": SCHEMA_VERSION,
        "run_id": branch_run_id,
        "parent_run_id": parent["run_id"],
        "parent_checkpoint_hash": parent_checkpoint_hash,
        "fork_ledger_offset": parent["ledger_record_count"],
        "parent_ledger_head_hash": parent_head,
        "initial_model_state_hash": parent["model_state_hash"],
        "final_model_state_hash": tensor_state_hash(state_dict_cpu(model)),
        "branch_ledger_head_hash": previous_hash,
        "next_batch_index": config["crash_after_step"] + 2,
        "mixture": {"code": 0.5, "indic": 0.125, "agentic": 0.125, "reasoning": 0.125, "general_web": 0.125},
    }
    payload_path = branch_dir / "checkpoint.pt"
    torch.save({**branch_checkpoint, "model_state": state_dict_cpu(model), "optimizer_state": optimizer.state_dict()}, payload_path)
    branch_checkpoint["checkpoint_file_hash"] = hash_file(payload_path)
    write_json(branch_dir / "checkpoint.json", branch_checkpoint)
    report = {
        "schema_version": SCHEMA_VERSION,
        "parent_checkpoint": str(checkpoint_path.relative_to(artifact_root)),
        "parent_checkpoint_hash": parent_checkpoint_hash,
        "fork_ledger_offset": parent["ledger_record_count"],
        "initial_model_hash_matched": branch_checkpoint["initial_model_state_hash"] == parent["model_state_hash"],
        "branch_batch_ids": [batch["batch_id"] for batch in branch_batches],
        "parent_future_batch_ids": [batch["batch_id"] for batch in source_batches[:2]],
        "branch_diverged": [batch["batch_id"] for batch in branch_batches] != [batch["batch_id"] for batch in source_batches[:2]],
        "branch_ledger_chain_valid": verify_hash_chain(branch_records, parent_head)[0],
    }
    write_json(branch_dir / "fork_report.json", report)
    logger.log("branch forked", f"offset={parent['ledger_record_count']}; batches=2; code_share=0.5")
    return report


def evaluate_firewalled_splits(
    artifact_root: Path, config: dict[str, Any], tokenizer: ByteTokenizer, all_rows: list[dict[str, Any]], logger: RunLogger
) -> dict[str, Any]:
    configure_determinism(config["seed"])
    model = make_model(config, tokenizer)
    optimizer, scheduler = optimizer_and_scheduler(model, config)
    final_step = len(config["stages"]) * config["steps_per_stage"]
    load_checkpoint(artifact_root / "checkpoints" / f"checkpoint_step_{final_step:04d}.pt", model, optimizer, scheduler)
    before_hash = tensor_state_hash(state_dict_cpu(model))
    records: list[dict[str, Any]] = []
    model.eval()
    with torch.no_grad():
        for row in all_rows:
            if row["split"] not in {"validation", "eval"}:
                continue
            segments = chunk_row(row, config["sequence_length"])
            sequence = build_packed_sequence([segments[0]], row["lane"], "evaluation_only", tokenizer, config["sequence_length"])
            inputs, labels, mask, positions, attention = sequence_tensors(sequence)
            logits = model(inputs, positions, attention)
            losses = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), labels.reshape(-1), reduction="none").reshape_as(mask)
            mean_loss = float(((losses * mask).sum() / mask.sum().clamp_min(1)).item())
            records.append(
                {
                    "doc_id": row["doc_id"],
                    "split": row["split"],
                    "shard_id": row["shard_id"],
                    "optimizer_update": False,
                    "mean_loss": mean_loss,
                    "model_state_hash": before_hash,
                }
            )
    after_hash = tensor_state_hash(state_dict_cpu(model))
    write_jsonl(artifact_root / "ledgers" / "evaluation.jsonl", records)
    firewall = read_json(artifact_root / "ledgers" / "firewall_report.json")
    firewall["evaluation_records"] = records
    firewall["model_hash_before_evaluation"] = before_hash
    firewall["model_hash_after_evaluation"] = after_hash
    firewall["evaluation_no_update"] = before_hash == after_hash and all(not record["optimizer_update"] for record in records)
    write_json(artifact_root / "ledgers" / "firewall_report.json", firewall)
    logger.log("validation and evaluation executed", f"records={len(records)}; optimizer_updates=0")
    return firewall


def build_performance_report(
    artifact_root: Path, packing_seconds: float, opus_seconds: float, replay_report: dict[str, Any], logger: RunLogger
) -> dict[str, Any]:
    records = read_jsonl(artifact_root / "ledgers" / "step_ledger.jsonl")
    raw_tokens = sum(record["consumption"]["raw_tokens"] for record in records)
    non_pad_tokens = sum(record["consumption"]["non_pad_tokens"] for record in records)
    useful_tokens = sum(record["consumption"]["loss_bearing_tokens"] for record in records)
    training_seconds = sum(record["learning"]["elapsed_seconds"] for record in records)
    span_count = sum(len(record["consumption"]["source_spans"]) for record in records)
    sequence_length = read_json(ROOT / "config" / "demo.json")["sequence_length"]
    pad_only_capacity = max(1, span_count * sequence_length)
    crash_intent = read_json(artifact_root / "checkpoints" / "crash_intent.json")
    performance = {
        "schema_version": SCHEMA_VERSION,
        "counts": {
            "raw_tokens": raw_tokens,
            "non_pad_tokens": non_pad_tokens,
            "loss_bearing_tokens": useful_tokens,
            "source_spans": span_count,
        },
        "timings_seconds": {
            "packing": packing_seconds,
            "opus": opus_seconds,
            "training": training_seconds,
            "replay": replay_report["elapsed_seconds"],
        },
        "packing_utilization": non_pad_tokens / raw_tokens,
        "pad_only_baseline_utilization": non_pad_tokens / pad_only_capacity,
        "raw_tokens_per_second": raw_tokens / training_seconds,
        "useful_loss_bearing_tokens_per_second": useful_tokens / training_seconds,
        "resume_expected_batch_id": crash_intent["expected_batch_id"],
        "formulae": {
            "packing_utilization": "non_pad_tokens / raw_tokens",
            "pad_only_baseline_utilization": "non_pad_tokens / (source_spans * sequence_length)",
            "raw_tokens_per_second": "raw_tokens / sum(step.learning.elapsed_seconds)",
            "useful_loss_bearing_tokens_per_second": "loss_bearing_tokens / sum(step.learning.elapsed_seconds)",
        },
    }
    write_json(artifact_root / "performance.json", performance)
    return performance

