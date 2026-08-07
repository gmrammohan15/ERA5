from __future__ import annotations

import math
from collections import Counter
from typing import Any, Iterable

from .common import SCHEMA_VERSION, sha256_json
from .packing import PROTECTED_LANES

def largest_remainder_quotas(weights: dict[str, float], total: int, minimums: dict[str, int]) -> dict[str, int]:
    quotas = {lane: max(minimums.get(lane, 0), math.floor(weight * total)) for lane, weight in weights.items()}
    while sum(quotas.values()) > total:
        candidates = [lane for lane in quotas if quotas[lane] > minimums.get(lane, 0)]
        lane = min(candidates, key=lambda name: (weights[name] * total - quotas[name], name))
        quotas[lane] -= 1
    while sum(quotas.values()) < total:
        lane = max(weights, key=lambda name: (weights[name] * total - quotas[name], name))
        quotas[lane] += 1
    return quotas


def compile_lane_schedule(config: dict[str, Any]) -> tuple[list[list[str]], dict[str, list[list[str]]], dict[str, Any]]:
    batch_size = config["global_batch_size"]
    steps = config["steps_per_stage"]
    all_batches: list[list[str]] = []
    by_stage: dict[str, list[list[str]]] = {}
    report: dict[str, Any] = {"schema_version": SCHEMA_VERSION, "stages": []}
    for stage in config["stages"]:
        minimum_per_batch = {
            lane: math.ceil(config["protected_floors"][lane] * batch_size) for lane in PROTECTED_LANES
        }
        minimum_stage = {lane: value * steps for lane, value in minimum_per_batch.items()}
        quotas = largest_remainder_quotas(stage["weights"], batch_size * steps, minimum_stage)
        counts = Counter()
        batches: list[list[str]] = []
        for _ in range(steps):
            lanes = list(PROTECTED_LANES)
            counts.update(lanes)
            while len(lanes) < batch_size:
                processed_after = sum(counts.values()) + 1
                candidates = [lane for lane in stage["weights"] if counts[lane] < quotas[lane]]
                lane = max(candidates, key=lambda name: (stage["weights"][name] * processed_after - counts[name], name))
                lanes.append(lane)
                counts[lane] += 1
            batches.append(lanes)
        by_stage[stage["name"]] = batches
        all_batches.extend(batches)
        actual = {lane: counts[lane] / (batch_size * steps) for lane in stage["weights"]}
        report["stages"].append(
            {
                "stage": stage["name"],
                "planned_weights": stage["weights"],
                "planned_sequence_counts": quotas,
                "actual_sequence_counts": dict(counts),
                "actual_shares": actual,
                "per_batch_floor_counts": minimum_per_batch,
                "batches": batches,
            }
        )
    report["schedule_hash"] = sha256_json(report["stages"])
    return all_batches, by_stage, report


def assert_train_rows(rows: Iterable[dict[str, Any]], component: str) -> None:
    blocked = [row["doc_id"] for row in rows if row["split"] != "train"]
    if blocked:
        raise PermissionError(f"{component} blocked non-train documents: {blocked}")



