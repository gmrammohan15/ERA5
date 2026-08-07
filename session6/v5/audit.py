from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .common import SCHEMA_VERSION, hash_file, read_json, read_jsonl, sha256_json, write_json
from .data import ByteTokenizer, validate_manifests
from .packing import PROTECTED_LANES
from .training import load_batch, verify_hash_chain

def audit_artifacts(artifact_root: Path, config: dict[str, Any], tokenizer: ByteTokenizer) -> dict[str, Any]:
    checks: dict[str, dict[str, Any]] = {}

    def record(name: str, passed: bool, detail: str, evidence: list[str], measurements: dict[str, Any] | None = None) -> None:
        checks[name] = {
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "evidence": evidence,
            "measurements": measurements or {},
        }

    required = [
        "run.log",
        "performance.json",
        "manifests/shard_index.json",
        "ledgers/step_ledger.jsonl",
        "ledgers/consumption.jsonl",
        "ledgers/learning.jsonl",
        "ledgers/opus_decisions.jsonl",
        "replay/replay_report.json",
        "branches/fork_code_heavy/fork_report.json",
    ]
    missing = [path for path in required if not (artifact_root / path).exists()]
    record("end_to_end", not missing, "all required execution artifacts exist" if not missing else f"missing: {missing}", required)

    tokenizer_manifest = read_json(artifact_root / "manifests" / "tokenizer.manifest.json")
    roundtrip_samples = ["India", "भारत", "తెలుగు", "def f(x): return x + 1"]
    tokenizer_ok = tokenizer_manifest["tokenizer_hash"] == tokenizer.tokenizer_hash and all(
        tokenizer.decode(tokenizer.encode(sample)) == sample for sample in roundtrip_samples
    )
    record(
        "tokenizer_integrity",
        tokenizer_ok,
        "frozen tokenizer hash and multilingual byte round-trips verified",
        ["manifests/tokenizer.manifest.json"],
        {"tokenizer_hash": tokenizer.tokenizer_hash, "roundtrip_samples": len(roundtrip_samples)},
    )

    manifest_ok = True
    manifest_count = 0
    try:
        validated_rows = validate_manifests(artifact_root, tokenizer)
        manifest_count = len(read_json(artifact_root / "manifests" / "shard_index.json")["shards"])
    except Exception as error:
        validated_rows = []
        manifest_ok = False
        manifest_error = str(error)
    else:
        manifest_error = "all content, tokenizer, cleaning and token-count hashes match"
    record(
        "shard_manifest_integrity",
        manifest_ok,
        manifest_error,
        ["manifests/shard_index.json", "shards/"],
        {"manifest_count": manifest_count},
    )

    firewall = read_json(artifact_root / "ledgers" / "firewall_report.json")
    step_records = read_jsonl(artifact_root / "ledgers" / "step_ledger.jsonl")
    consumed_shards = {
        span["shard_id"] for item in step_records for span in item["consumption"]["source_spans"]
    }
    forbidden_consumption = sorted(
        shard for shard in consumed_shards if shard.startswith(("eval-", "validation-", "selection_proxy-"))
    )
    firewall_ok = (
        firewall.get("eval_attempt_blocked")
        and firewall.get("validation_attempt_blocked")
        and firewall.get("evaluation_no_update")
        and not forbidden_consumption
    )
    record(
        "evaluation_firewall",
        bool(firewall_ok),
        "eval and validation were rejected from training and evaluated without parameter updates",
        ["ledgers/firewall_report.json", "ledgers/evaluation.jsonl", "ledgers/consumption.jsonl"],
        {"forbidden_training_shards": forbidden_consumption},
    )

    packing_ok = True
    sequence_count = 0
    policy_counts: Counter[str] = Counter()
    for batch_index in range(len(config["stages"]) * config["steps_per_stage"]):
        batch = load_batch(artifact_root, batch_index)
        tensor_view = [
            {
                key: sequence[key]
                for key in ("input_ids", "labels", "loss_mask", "attention_mask", "position_ids", "segment_ids", "source_spans")
            }
            for sequence in batch["sequences"]
        ]
        packing_ok &= sha256_json(tensor_view) == batch["tensor_hash"]
        for sequence in batch["sequences"]:
            sequence_count += 1
            policy_counts[sequence["packing_policy"]] += 1
            length = config["sequence_length"]
            packing_ok &= all(len(sequence[key]) == length for key in ("input_ids", "labels", "loss_mask", "position_ids", "segment_ids"))
            packing_ok &= len(sequence["attention_mask"]) == length and all(len(row) == length for row in sequence["attention_mask"])
            for position, role in enumerate(sequence["token_roles"][:-1]):
                if role == "pad":
                    packing_ok &= sequence["loss_mask"][position] == 0
            for query in range(length):
                for key in range(query + 1, length):
                    packing_ok &= not sequence["attention_mask"][query][key]
            for query in range(length - 1):
                if sequence["segment_ids"][query] != sequence["segment_ids"][query + 1]:
                    packing_ok &= sequence["loss_mask"][query] == 0
    expected_policies = {"best_fit", "greedy", "structure_preserving"}
    packing_ok &= expected_policies.issubset(policy_counts)
    record(
        "packing_correctness",
        bool(packing_ok),
        "tensor hashes, causal masks, segment boundaries, padding masks and position shapes verified",
        ["batches/", "performance/packing_report.json"],
        {"sequence_count": sequence_count, "policy_counts": dict(policy_counts)},
    )

    schedule = read_json(artifact_root / "manifests" / "mixture_schedule.json")
    mixture_ok = True
    floor_ok = True
    for stage_position, stage_report in enumerate(schedule["stages"]):
        start = stage_position * config["steps_per_stage"]
        batches = [load_batch(artifact_root, index) for index in range(start, start + config["steps_per_stage"])]
        observed = Counter(sequence["lane"] for batch in batches for sequence in batch["sequences"])
        mixture_ok &= dict(observed) == stage_report["actual_sequence_counts"]
        for batch in batches:
            for lane in PROTECTED_LANES:
                minimum = stage_report["per_batch_floor_counts"][lane]
                floor_ok &= batch["lane_counts"].get(lane, 0) >= minimum
    record(
        "mixture_compliance",
        bool(mixture_ok),
        "observed stage lane counts equal the compiled schedule",
        ["manifests/mixture_schedule.json", "ledgers/consumption.jsonl"],
    )
    record(
        "protected_floors",
        bool(floor_ok),
        "Indic, agentic and reasoning floors hold in every global batch",
        ["manifests/mixture_schedule.json", "batches/"],
    )

    opus = read_jsonl(artifact_root / "ledgers" / "opus_decisions.jsonl")
    base_statuses = {record["base_decision"] for record in opus}
    override_count = sum(bool(record["protected_floor_override"]) for record in opus)
    opus_ok = {"accepted", "rejected", "deferred"}.issubset(base_statuses) and override_count > 0
    record(
        "opus_audit_trail",
        opus_ok,
        "gradient-alignment decisions include acceptance, rejection, deferral and protected override",
        ["ledgers/opus_decisions.jsonl"],
        {"base_statuses": sorted(base_statuses), "protected_overrides": override_count, "decision_count": len(opus)},
    )

    chain_ok, head = verify_hash_chain(step_records)
    expected_indices = list(range(len(config["stages"]) * config["steps_per_stage"]))
    observed_indices = [record["global_step"] for record in step_records]
    consumption = read_jsonl(artifact_root / "ledgers" / "consumption.jsonl")
    learning = read_jsonl(artifact_root / "ledgers" / "learning.jsonl")
    ledger_ok = chain_ok and observed_indices == expected_indices and len(consumption) == len(learning) == len(step_records)
    projection_ok = all(
        consumption[index]["step_record_hash"] == record["record_hash"]
        and learning[index]["step_record_hash"] == record["record_hash"]
        for index, record in enumerate(step_records)
    )
    record(
        "consumption_ledger",
        ledger_ok and projection_ok,
        "hash chain, contiguous batch indices and consumption/learning projections verified",
        ["ledgers/step_ledger.jsonl", "ledgers/consumption.jsonl", "ledgers/learning.jsonl"],
        {"records": len(step_records), "ledger_head_hash": head},
    )
    trace_ok = all(
        item["learning"]["token_losses"]
        and all(trace["doc_id"] and trace["shard_id"] for trace in item["learning"]["token_losses"])
        and len(item["learning"]["sample_losses"]) == config["global_batch_size"]
        for item in step_records
    )
    record(
        "learning_trace",
        trace_ok,
        "real token/sample losses and gradients link back to source documents",
        ["ledgers/learning.jsonl", "ledgers/step_ledger.jsonl"],
        {"token_loss_records": sum(len(item["learning"]["token_losses"]) for item in step_records)},
    )

    crash_step = config["crash_after_step"]
    crash_meta = read_json(artifact_root / "checkpoints" / f"checkpoint_step_{crash_step:04d}.json")
    final_meta = read_json(artifact_root / "checkpoints" / f"checkpoint_step_{len(expected_indices):04d}.json")
    checkpoint_ok = (
        crash_meta["ledger_record_count"] == crash_step
        and final_meta["ledger_record_count"] == len(expected_indices)
        and final_meta["ledger_head_hash"] == head
        and hash_file(artifact_root / final_meta["checkpoint_file"]) == final_meta["checkpoint_file_hash"]
    )
    record(
        "checkpoint_integrity",
        checkpoint_ok,
        "checkpoint model/data state is tied to exact ledger offsets and hashes",
        [f"checkpoints/checkpoint_step_{crash_step:04d}.json", f"checkpoints/checkpoint_step_{len(expected_indices):04d}.json"],
    )
    intent = read_json(artifact_root / "checkpoints" / "crash_intent.json")
    resumed_record = step_records[crash_step]
    resume_ok = (
        resumed_record["consumption"]["batch_id"] == intent["expected_batch_id"]
        and resumed_record["consumption"]["tensor_hash"] == intent["expected_tensor_hash"]
        and observed_indices == expected_indices
    )
    record(
        "crash_recovery",
        resume_ok,
        "fresh process consumed the exact expected next batch with no skip or duplicate",
        ["checkpoints/crash_intent.json", "ledgers/step_ledger.jsonl", "run.log"],
        {"expected_batch_id": intent["expected_batch_id"], "resumed_batch_id": resumed_record["consumption"]["batch_id"]},
    )

    replay = read_json(artifact_root / "replay" / "replay_report.json")
    record(
        "replay",
        bool(replay["all_matched"]),
        "historical batch ids, token spans, tensor hashes, losses and model hashes match",
        ["replay/replay_report.json"],
        {"interval": replay["interval"], "batches": len(replay["comparisons"])},
    )
    fork = read_json(artifact_root / "branches" / "fork_code_heavy" / "fork_report.json")
    fork_ok = fork["initial_model_hash_matched"] and fork["branch_diverged"] and fork["branch_ledger_chain_valid"]
    record(
        "fork",
        fork_ok,
        "branch preserves parent checkpoint lineage and diverges under a code-heavy future mixture",
        ["branches/fork_code_heavy/fork_report.json", "branches/fork_code_heavy/checkpoint.json"],
    )

    performance = read_json(artifact_root / "performance.json")
    counts = performance["counts"]
    recalculated = {
        "raw_tokens": sum(item["consumption"]["raw_tokens"] for item in step_records),
        "non_pad_tokens": sum(item["consumption"]["non_pad_tokens"] for item in step_records),
        "loss_bearing_tokens": sum(item["consumption"]["loss_bearing_tokens"] for item in step_records),
    }
    elapsed = sum(item["learning"]["elapsed_seconds"] for item in step_records)
    performance_ok = (
        all(counts[key] == value for key, value in recalculated.items())
        and abs(performance["packing_utilization"] - recalculated["non_pad_tokens"] / recalculated["raw_tokens"]) < 1e-12
        and abs(performance["useful_loss_bearing_tokens_per_second"] - recalculated["loss_bearing_tokens"] / elapsed) < 1e-9
        and performance["useful_loss_bearing_tokens_per_second"] > 0
    )
    record(
        "throughput",
        performance_ok,
        "packing and useful-token throughput claims reconstruct from batch and learning records",
        ["performance.json", "ledgers/step_ledger.jsonl"],
        {
            "packing_utilization": performance["packing_utilization"],
            "useful_tokens_per_second": performance["useful_loss_bearing_tokens_per_second"],
        },
    )

    audit = {
        "schema_version": SCHEMA_VERSION,
        "checks": checks,
        "all_passed": all(check["result"] == "PASS" for check in checks.values()),
        "audit_hash": sha256_json(checks),
    }
    write_json(artifact_root / "ledgers" / "audit_report.json", audit)
    return audit


def generate_evidence(artifact_root: Path, audit: dict[str, Any]) -> dict[str, Any]:
    requirements = {
        "end_to_end_execution": ["end_to_end"],
        "tokenizer_integrity": ["tokenizer_integrity", "shard_manifest_integrity"],
        "evaluation_firewall": ["evaluation_firewall"],
        "packing_correctness": ["packing_correctness"],
        "mixture_compliance": ["mixture_compliance", "protected_floors"],
        "opus_audit_trail": ["opus_audit_trail"],
        "consumption_and_learning_ledgers": ["consumption_ledger"],
        "learning_trace": ["learning_trace"],
        "checkpoint_integrity": ["checkpoint_integrity"],
        "crash_recovery": ["crash_recovery"],
        "replay": ["replay"],
        "fork": ["fork"],
        "throughput": ["throughput"],
    }
    rendered: dict[str, Any] = {}
    for requirement, names in requirements.items():
        selected = [audit["checks"][name] for name in names]
        rendered[requirement] = {
            "result": "PASS" if all(item["result"] == "PASS" for item in selected) else "FAIL",
            "audit_checks": names,
            "evidence": sorted({path for item in selected for path in item["evidence"]}),
            "measurements": {name: audit["checks"][name]["measurements"] for name in names},
        }
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "generated_from_audit_hash": audit["audit_hash"],
        "all_passed": all(item["result"] == "PASS" for item in rendered.values()),
        "requirements": rendered,
    }
    write_json(artifact_root / "evidence.json", evidence)
    labels = [
        ("Tokenizer integrity", "tokenizer_integrity"),
        ("Evaluation firewall", "evaluation_firewall"),
        ("Packing correctness", "packing_correctness"),
        ("Mixture compliance", "mixture_compliance"),
        ("OPUS audit trail", "opus_audit_trail"),
        ("Crash recovery", "crash_recovery"),
        ("Replay", "replay"),
        ("Learning trace", "learning_trace"),
        ("Throughput", "throughput"),
    ]
    lines = ["# V5 Execution Evidence", "", "| Requirement | Result | Evidence |", "|---|---|---|"]
    for label, key in labels:
        item = rendered[key]
        lines.append(f"| {label} | {item['result']} | {', '.join(item['evidence'])} |")
    lines.extend(["", f"Overall result: **{'PASS' if evidence['all_passed'] else 'FAIL'}**", ""])
    (artifact_root / "evidence.md").write_text("\n".join(lines), encoding="utf-8")
    return evidence

