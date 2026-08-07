from __future__ import annotations

import math
from collections import defaultdict
from pathlib import Path
from typing import Any

import torch
from torch.nn import functional as F

from .common import SCHEMA_VERSION, sha256_json, tensor_state_hash, write_jsonl
from .data import ByteTokenizer
from .interfaces import SampleSelectorProtocol
from .model import TinyCausalLM, state_dict_cpu
from .packing import PROTECTED_LANES, build_packed_sequence, chunk_row, sequence_tensors

def gradient_vector(model: TinyCausalLM, sequence: dict[str, Any]) -> torch.Tensor:
    inputs, labels, mask, positions, attention = sequence_tensors(sequence)
    logits = model(inputs, positions, attention)
    losses = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), labels.reshape(-1), reduction="none").reshape_as(mask)
    loss = (losses * mask).sum() / mask.sum().clamp_min(1)
    gradient = torch.autograd.grad(loss, model.lm_head.weight, retain_graph=False, create_graph=False)[0]
    return gradient.detach().flatten()


def score_opus(
    artifact_root: Path,
    config: dict[str, Any],
    tokenizer: ByteTokenizer,
    model: TinyCausalLM,
    all_rows: list[dict[str, Any]],
    lane_slots: dict[str, list[list[str]]],
) -> tuple[list[dict[str, Any]], dict[int, dict[str, list[dict[str, Any]]]]]:
    train_rows = [row for row in all_rows if row["split"] == "train"]
    proxy_rows = [row for row in all_rows if row["split"] == "selection_proxy"]
    proxy_segments: list[dict[str, Any]] = []
    for row in proxy_rows:
        chunk = chunk_row(row, config["sequence_length"])[0]
        chunk["tokens"] = chunk["tokens"][: config["opus_prefix_tokens"]]
        chunk["roles"] = chunk["roles"][: config["opus_prefix_tokens"]]
        proxy_segments.append(chunk)
    proxy_sequence = build_packed_sequence(
        proxy_segments[:3], "selection_proxy", "structure_preserving", tokenizer, config["sequence_length"]
    )
    reference_gradient = gradient_vector(model, proxy_sequence)
    model_hash = tensor_state_hash(state_dict_cpu(model))
    decisions: list[dict[str, Any]] = []
    admitted: dict[int, dict[str, list[dict[str, Any]]]] = defaultdict(dict)
    decision_counter = 0
    for stage in config["stages"]:
        stage_index = stage["index"]
        stage_decisions: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in train_rows:
            decision_id = f"opus-{stage_index:02d}-{decision_counter:04d}"
            decision_counter += 1
            if row["min_stage"] > stage_index:
                score = None
                base_decision = "deferred"
                reason = "stage_mismatch"
            else:
                segment = chunk_row(row, config["sequence_length"])[0]
                segment["tokens"] = segment["tokens"][: config["opus_prefix_tokens"]]
                segment["roles"] = segment["roles"][: config["opus_prefix_tokens"]]
                candidate = build_packed_sequence([segment], row["lane"], "opus_prefix", tokenizer, config["sequence_length"])
                candidate_gradient = gradient_vector(model, candidate)
                score = float(F.cosine_similarity(reference_gradient, candidate_gradient, dim=0).item())
                base_decision = "unranked"
                reason = "pending_lane_rank"
            record = {
                "schema_version": SCHEMA_VERSION,
                "decision_id": decision_id,
                "stage": stage["name"],
                "stage_index": stage_index,
                "doc_id": row["doc_id"],
                "lane": row["lane"],
                "candidate_prefix_tokens": min(len(row["tokens"]), config["opus_prefix_tokens"]),
                "gradient_alignment": score,
                "quality": row["quality"],
                "model_state_hash": model_hash,
                "base_decision": base_decision,
                "final_decision": base_decision,
                "reason": reason,
                "protected_floor_override": False,
                "shard_id": row["shard_id"],
                "row_id": row["row_id"],
            }
            decisions.append(record)
            stage_decisions[row["lane"]].append(record)
        for lane, lane_records in stage_decisions.items():
            eligible = [record for record in lane_records if record["base_decision"] == "unranked"]
            eligible.sort(key=lambda record: (-float(record["gradient_alignment"]), -record["quality"], record["doc_id"]))
            accepted_count = max(1, math.ceil(len(eligible) * 0.4)) if eligible else 0
            deferred_count = max(1, math.ceil(len(eligible) * 0.3)) if len(eligible) >= 3 else 0
            for rank, record in enumerate(eligible):
                record["alignment_rank"] = rank + 1
                if rank < accepted_count:
                    record["base_decision"] = record["final_decision"] = "accepted"
                    record["reason"] = "top_gradient_alignment"
                elif rank < accepted_count + deferred_count:
                    record["base_decision"] = record["final_decision"] = "deferred"
                    record["reason"] = "borderline_gradient_alignment"
                else:
                    record["base_decision"] = record["final_decision"] = "rejected"
                    record["reason"] = "low_gradient_alignment"
            accepted = [record for record in lane_records if record["final_decision"] == "accepted"]
            if lane in PROTECTED_LANES:
                required_exposures = sum(batch.count(lane) for batch in lane_slots[stage["name"]])
                eligible_count = sum(1 for record in lane_records if record["gradient_alignment"] is not None)
                required_unique = min(required_exposures, eligible_count)
                rescue_candidates = [
                    record
                    for record in eligible
                    if record["final_decision"] != "accepted"
                ]
                for record in rescue_candidates[: max(0, required_unique - len(accepted))]:
                    record["final_decision"] = "accepted_override"
                    record["protected_floor_override"] = True
                    record["reason"] = "protected_floor_override"
                    accepted.append(record)
            admitted_ids = {record["doc_id"] for record in lane_records if record["final_decision"] in {"accepted", "accepted_override"}}
            admitted[stage_index][lane] = [row for row in train_rows if row["lane"] == lane and row["doc_id"] in admitted_ids]
    write_jsonl(artifact_root / "ledgers" / "opus_decisions.jsonl", decisions)
    return decisions, admitted


class GradientAlignmentSelector(SampleSelectorProtocol):
    """Reusable OPUS-style selector backed by candidate/reference gradients."""

    def __init__(self, config: dict[str, Any], tokenizer: ByteTokenizer):
        self.config = config
        self.tokenizer = tokenizer

    def select(
        self,
        artifact_root: Path,
        model: TinyCausalLM,
        rows: list[dict[str, Any]],
        lane_slots: dict[str, list[list[str]]],
    ) -> tuple[list[dict[str, Any]], dict[int, dict[str, list[dict[str, Any]]]]]:
        return score_opus(artifact_root, self.config, self.tokenizer, model, rows, lane_slots)



