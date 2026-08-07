from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .common import SCHEMA_VERSION, sha256_json, write_json
from .curriculum import assert_train_rows
from .data import ByteTokenizer
from .packing import pack_rows

def make_batch(batch_index: int, stage: dict[str, Any], sequences: list[dict[str, Any]], schedule_hash: str) -> dict[str, Any]:
    core = {
        "schema_version": SCHEMA_VERSION,
        "batch_index": batch_index,
        "stage": stage["name"],
        "stage_index": stage["index"],
        "schedule_hash": schedule_hash,
        "sequence_hashes": [sequence["sequence_hash"] for sequence in sequences],
        "sequences": sequences,
        "raw_tokens": len(sequences) * len(sequences[0]["input_ids"]),
        "non_pad_tokens": sum(sequence["non_pad_tokens"] for sequence in sequences),
        "loss_bearing_tokens": sum(sequence["loss_bearing_tokens"] for sequence in sequences),
        "lane_counts": dict(Counter(sequence["lane"] for sequence in sequences)),
    }
    tensor_view = [
        {
            key: sequence[key]
            for key in ("input_ids", "labels", "loss_mask", "attention_mask", "position_ids", "segment_ids", "source_spans")
        }
        for sequence in sequences
    ]
    core["tensor_hash"] = sha256_json(tensor_view)
    core["batch_id"] = f"batch-{batch_index:04d}-{sha256_json(core)[:16]}"
    return core


def build_batches(
    artifact_root: Path,
    config: dict[str, Any],
    tokenizer: ByteTokenizer,
    admitted: dict[int, dict[str, list[dict[str, Any]]]],
    decisions: list[dict[str, Any]],
    lane_batches: list[list[str]],
    schedule_report: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    decision_by_stage_doc = {(record["stage_index"], record["doc_id"]): record for record in decisions}
    pools: dict[tuple[int, str], list[dict[str, Any]]] = {}
    packing_rows: list[dict[str, Any]] = []
    for stage in config["stages"]:
        for lane in stage["weights"]:
            rows = admitted[stage["index"]].get(lane, [])
            assert_train_rows(rows, "packer")
            if not rows:
                raise ValueError(f"no admitted rows for stage={stage['name']} lane={lane}")
            doc_decisions = {
                row["doc_id"]: decision_by_stage_doc[(stage["index"], row["doc_id"])]["decision_id"] for row in rows
            }
            pool = pack_rows(rows, lane, tokenizer, config["sequence_length"], doc_decisions)
            pools[(stage["index"], lane)] = pool
            for sequence in pool:
                packing_rows.append(
                    {
                        "stage": stage["name"],
                        "lane": lane,
                        "packing_policy": sequence["packing_policy"],
                        "sequence_hash": sequence["sequence_hash"],
                        "raw_tokens": config["sequence_length"],
                        "non_pad_tokens": sequence["non_pad_tokens"],
                        "loss_bearing_tokens": sequence["loss_bearing_tokens"],
                        "utilization": sequence["non_pad_tokens"] / config["sequence_length"],
                        "source_spans": sequence["source_spans"],
                    }
                )
    cursors: Counter[tuple[int, str]] = Counter()
    batches: list[dict[str, Any]] = []
    for batch_index, lanes in enumerate(lane_batches):
        stage = config["stages"][batch_index // config["steps_per_stage"]]
        sequences: list[dict[str, Any]] = []
        for lane in lanes:
            key = (stage["index"], lane)
            pool = pools[key]
            sequence = pool[cursors[key] % len(pool)]
            cursors[key] += 1
            sequences.append(sequence)
        batch = make_batch(batch_index, stage, sequences, schedule_report["schedule_hash"])
        write_json(artifact_root / "batches" / f"batch_{batch_index:04d}.json", batch)
        batches.append(batch)
    totals = {
        "raw_tokens": sum(row["raw_tokens"] for row in packing_rows),
        "non_pad_tokens": sum(row["non_pad_tokens"] for row in packing_rows),
        "loss_bearing_tokens": sum(row["loss_bearing_tokens"] for row in packing_rows),
    }
    packing_report = {
        "schema_version": SCHEMA_VERSION,
        "sequences": packing_rows,
        "totals": totals,
        "packing_utilization": totals["non_pad_tokens"] / totals["raw_tokens"],
        "useful_loss_fraction": totals["loss_bearing_tokens"] / totals["raw_tokens"],
    }
    write_json(artifact_root / "performance" / "packing_report.json", packing_report)
    write_json(artifact_root / "batches" / "batch_index.json", {"batches": [{"batch_index": b["batch_index"], "batch_id": b["batch_id"], "tensor_hash": b["tensor_hash"]} for b in batches]})
    write_json(artifact_root / "manifests" / "mixture_schedule.json", schedule_report)
    return batches, packing_report


