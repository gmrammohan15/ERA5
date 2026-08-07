from __future__ import annotations

import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import torch
from torch.nn import functional as F

from .common import SCHEMA_VERSION, sha256_json, tensor_state_hash, write_json, write_jsonl
from .data import ByteTokenizer
from .interfaces import PackingPolicyProtocol, SampleSelectorProtocol
from .model import TinyCausalLM, state_dict_cpu


LOSS_BEARING_ROLES = {"content", "assistant", "tool_call", "eos"}
PROTECTED_LANES = ("indic", "agentic", "reasoning")


def chunk_row(row: dict[str, Any], sequence_length: int) -> list[dict[str, Any]]:
    capacity = sequence_length - 2
    chunks: list[dict[str, Any]] = []
    for start in range(0, len(row["tokens"]), capacity):
        end = min(start + capacity, len(row["tokens"]))
        chunks.append(
            {
                "tokens": row["tokens"][start:end],
                "roles": row["roles"][start:end],
                "ref": {
                    "shard_id": row["shard_id"],
                    "row_id": row["row_id"],
                    "doc_id": row["doc_id"],
                    "token_start": start,
                    "token_end": end,
                    "span_hash": sha256_json(row["tokens"][start:end]),
                },
            }
        )
    return chunks


def build_packed_sequence(
    segments: list[dict[str, Any]],
    lane: str,
    policy: str,
    tokenizer: ByteTokenizer,
    sequence_length: int,
    decision_ids: list[str] | None = None,
) -> dict[str, Any]:
    input_ids: list[int] = []
    token_roles: list[str] = []
    segment_ids: list[int] = []
    position_ids: list[int] = []
    refs: list[dict[str, Any]] = []
    for segment_index, segment in enumerate(segments):
        segment_tokens = [tokenizer.bos_id, *segment["tokens"], tokenizer.eos_id]
        segment_roles = ["bos", *segment["roles"], "eos"]
        if len(input_ids) + len(segment_tokens) > sequence_length:
            raise ValueError("packed segment exceeds sequence length")
        offset = len(input_ids)
        input_ids.extend(segment_tokens)
        token_roles.extend(segment_roles)
        segment_ids.extend([segment_index] * len(segment_tokens))
        position_ids.extend(range(len(segment_tokens)))
        refs.append({**segment["ref"], "segment_id": segment_index, "packed_start": offset, "packed_end": offset + len(segment_tokens)})
    non_pad_tokens = len(input_ids)
    padding = sequence_length - non_pad_tokens
    input_ids.extend([tokenizer.pad_id] * padding)
    token_roles.extend(["pad"] * padding)
    segment_ids.extend([-1] * padding)
    position_ids.extend([0] * padding)
    labels = [tokenizer.pad_id] * sequence_length
    loss_mask = [0] * sequence_length
    for index in range(sequence_length - 1):
        labels[index] = input_ids[index + 1]
        same_segment = segment_ids[index] >= 0 and segment_ids[index] == segment_ids[index + 1]
        if same_segment and token_roles[index + 1] in LOSS_BEARING_ROLES:
            loss_mask[index] = 1
    attention_mask: list[list[bool]] = []
    for query in range(sequence_length):
        row_mask: list[bool] = []
        for key in range(sequence_length):
            if segment_ids[query] < 0:
                allowed = key == query
            else:
                allowed = segment_ids[key] == segment_ids[query] and key <= query
            row_mask.append(allowed)
        attention_mask.append(row_mask)
    sequence_core = {
        "schema_version": SCHEMA_VERSION,
        "lane": lane,
        "packing_policy": policy,
        "input_ids": input_ids,
        "labels": labels,
        "loss_mask": loss_mask,
        "attention_mask": attention_mask,
        "position_ids": position_ids,
        "segment_ids": segment_ids,
        "token_roles": token_roles,
        "source_spans": refs,
        "non_pad_tokens": non_pad_tokens,
        "loss_bearing_tokens": sum(loss_mask),
        "opus_decision_ids": decision_ids or [],
    }
    sequence_core["sequence_hash"] = sha256_json(sequence_core)
    return sequence_core


class PackingPolicyRegistry(PackingPolicyProtocol):
    """Configurable lane-to-policy registry used by the reference packer."""

    def __init__(self, policies: dict[str, str] | None = None, default: str = "greedy"):
        self._policies = policies or {
            "general_web": "best_fit",
            "indic": "best_fit",
            "agentic": "structure_preserving",
        }
        self._default = default

    def register(self, lane: str, policy: str) -> None:
        if policy not in {"best_fit", "greedy", "structure_preserving"}:
            raise ValueError(f"unknown packing policy: {policy}")
        self._policies[lane] = policy

    def policy_for(self, lane: str) -> str:
        return self._policies.get(lane, self._default)


DEFAULT_PACKING_POLICIES = PackingPolicyRegistry()


def packing_policy(lane: str) -> str:
    return DEFAULT_PACKING_POLICIES.policy_for(lane)


def pack_rows(
    rows: list[dict[str, Any]],
    lane: str,
    tokenizer: ByteTokenizer,
    sequence_length: int,
    decision_by_doc: dict[str, str],
) -> list[dict[str, Any]]:
    policy = packing_policy(lane)
    chunks = [chunk for row in sorted(rows, key=lambda item: item["doc_id"]) for chunk in chunk_row(row, sequence_length)]
    bins: list[list[dict[str, Any]]] = []
    if policy == "structure_preserving":
        bins = [[chunk] for chunk in chunks]
    elif policy == "greedy":
        current: list[dict[str, Any]] = []
        used = 0
        for chunk in chunks:
            size = len(chunk["tokens"]) + 2
            if current and used + size > sequence_length:
                bins.append(current)
                current, used = [], 0
            current.append(chunk)
            used += size
        if current:
            bins.append(current)
    else:
        for chunk in sorted(chunks, key=lambda item: (-len(item["tokens"]), item["ref"]["doc_id"], item["ref"]["token_start"])):
            size = len(chunk["tokens"]) + 2
            best_index: int | None = None
            best_remaining: int | None = None
            for index, existing in enumerate(bins):
                used = sum(len(item["tokens"]) + 2 for item in existing)
                remaining = sequence_length - used
                if size <= remaining and (best_remaining is None or remaining - size < best_remaining):
                    best_index = index
                    best_remaining = remaining - size
            if best_index is None:
                bins.append([chunk])
            else:
                bins[best_index].append(chunk)
    packed: list[dict[str, Any]] = []
    for segments in bins:
        decision_ids = sorted({decision_by_doc[segment["ref"]["doc_id"]] for segment in segments})
        packed.append(build_packed_sequence(segments, lane, policy, tokenizer, sequence_length, decision_ids))
    if policy == "best_fit":
        # Exercise dense multi-document packs early in the deterministic stream;
        # otherwise long-document chunks can hide the utilization gain in a tiny demo.
        packed.sort(key=lambda sequence: (-len(sequence["source_spans"]), -sequence["non_pad_tokens"], sequence["sequence_hash"]))
    return packed


def sequence_tensors(sequence: dict[str, Any]) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    return (
        torch.tensor(sequence["input_ids"], dtype=torch.long).unsqueeze(0),
        torch.tensor(sequence["labels"], dtype=torch.long).unsqueeze(0),
        torch.tensor(sequence["loss_mask"], dtype=torch.float32).unsqueeze(0),
        torch.tensor(sequence["position_ids"], dtype=torch.long).unsqueeze(0),
        torch.tensor(sequence["attention_mask"], dtype=torch.bool).unsqueeze(0),
    )



