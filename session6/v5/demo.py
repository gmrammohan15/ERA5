from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

from .audit import audit_artifacts, generate_evidence
from .batches import build_batches
from .common import CRASH_EXIT_CODE, ROOT, SCHEMA_VERSION, RunLogger, configure_determinism, read_json, sha256_json, write_json, write_jsonl
from .curriculum import assert_train_rows, compile_lane_schedule
from .data import ByteTokenizer, build_shards, load_documents, validate_manifests
from .model import make_model
from .recovery import build_performance_report, create_fork, evaluate_firewalled_splits, replay_history
from .selection import GradientAlignmentSelector
from .training import optimizer_and_scheduler, save_checkpoint

def run_demo(output: Path) -> int:
    output = output.resolve()
    staging = output.with_name(f".{output.name}.staging")
    backup = output.with_name(f".{output.name}.previous")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    logger = RunLogger(staging / "run.log")
    config = read_json(ROOT / "config" / "demo.json")
    tokenizer = ByteTokenizer(read_json(ROOT / "config" / "tokenizer.json"))
    configure_determinism(config["seed"])
    logger.log("demo started", f"seed={config['seed']}; device=cpu")
    documents = load_documents(ROOT / "data" / "documents.jsonl")
    shard_index = build_shards(staging, documents, tokenizer)
    logger.log("shards created", f"count={len(shard_index['shards'])}")
    all_rows = validate_manifests(staging, tokenizer)
    logger.log("manifests validated", f"rows={len(all_rows)}")
    logger.log("tokenizer_hash_verified", tokenizer.tokenizer_hash, "PASS")

    eval_rows = [row for row in all_rows if row["split"] == "eval"]
    validation_rows = [row for row in all_rows if row["split"] == "validation"]
    eval_blocked = validation_blocked = False
    eval_reason = validation_reason = ""
    try:
        assert_train_rows(eval_rows, "mixture_compiler")
    except PermissionError as error:
        eval_blocked, eval_reason = True, str(error)
    try:
        assert_train_rows(validation_rows, "trainer")
    except PermissionError as error:
        validation_blocked, validation_reason = True, str(error)
    split_hashes: dict[str, set[str]] = defaultdict(set)
    for row in all_rows:
        split_hashes[row["split"]].add(row["cleaned_content_hash"])
    overlaps = sorted(split_hashes["train"] & (split_hashes["eval"] | split_hashes["validation"]))
    firewall_report = {
        "schema_version": SCHEMA_VERSION,
        "eval_attempt_blocked": eval_blocked,
        "eval_block_reason": eval_reason,
        "validation_attempt_blocked": validation_blocked,
        "validation_block_reason": validation_reason,
        "train_eval_validation_content_overlaps": overlaps,
    }
    write_json(staging / "ledgers" / "firewall_report.json", firewall_report)
    if eval_blocked and not overlaps:
        logger.log("evaluation data blocked", eval_reason)
        logger.log("eval_shard_blocked", eval_rows[0]["shard_id"], "PASS")

    lane_batches, by_stage, schedule_report = compile_lane_schedule(config)
    logger.log("mixture compiled", f"stages={len(config['stages'])}; batches={len(lane_batches)}")
    model = make_model(config, tokenizer)
    opus_started = time.perf_counter()
    selector = GradientAlignmentSelector(config, tokenizer)
    decisions, admitted = selector.select(staging, model, all_rows, by_stage)
    opus_seconds = time.perf_counter() - opus_started
    logger.log(
        "OPUS decisions recorded",
        f"accepted={sum(d['base_decision']=='accepted' for d in decisions)}; rejected={sum(d['base_decision']=='rejected' for d in decisions)}; deferred={sum(d['base_decision']=='deferred' for d in decisions)}; overrides={sum(d['protected_floor_override'] for d in decisions)}",
    )
    packing_started = time.perf_counter()
    batches, _ = build_batches(staging, config, tokenizer, admitted, decisions, lane_batches, schedule_report)
    packing_seconds = time.perf_counter() - packing_started
    logger.log("batches packed", f"count={len(batches)}; sequence_length={config['sequence_length']}")

    (staging / "ledgers").mkdir(parents=True, exist_ok=True)
    write_jsonl(staging / "ledgers" / "step_ledger.jsonl", [])
    optimizer, scheduler = optimizer_and_scheduler(model, config)
    run_id = "run-" + sha256_json({"config": config, "tokenizer": tokenizer.tokenizer_hash, "manifests": shard_index["index_hash"]})[:16]
    save_checkpoint(
        staging,
        "checkpoint_genesis",
        model,
        optimizer,
        scheduler,
        0,
        sha256_json(config),
        tokenizer.tokenizer_hash,
        shard_index["index_hash"],
        run_id,
        logger,
    )

    environment = dict(os.environ)
    environment["PYTHONHASHSEED"] = str(config["seed"])
    crash_command = [sys.executable, str(ROOT / "run_demo.py"), "--worker", "crash", "--artifact-root", str(staging)]
    crashed = subprocess.run(crash_command, cwd=ROOT, env=environment, check=False)
    if crashed.returncode != CRASH_EXIT_CODE:
        raise RuntimeError(f"expected crash exit {CRASH_EXIT_CODE}, got {crashed.returncode}")
    resume_command = [sys.executable, str(ROOT / "run_demo.py"), "--worker", "resume", "--artifact-root", str(staging)]
    resumed = subprocess.run(resume_command, cwd=ROOT, env=environment, check=False)
    if resumed.returncode != 0:
        raise RuntimeError(f"resume worker failed with exit {resumed.returncode}")

    replay_report = replay_history(staging, config, tokenizer, all_rows, logger)
    create_fork(staging, config, tokenizer, logger)
    evaluate_firewalled_splits(staging, config, tokenizer, all_rows, logger)
    build_performance_report(staging, packing_seconds, opus_seconds, replay_report, logger)
    audit = audit_artifacts(staging, config, tokenizer)
    evidence = generate_evidence(staging, audit)
    logger.log("audit completed", f"checks={len(audit['checks'])}; all_passed={audit['all_passed']}")
    logger.log("performance measured", "performance.json generated from ledger timings")
    for name, result in audit["checks"].items():
        logger.log(name, result["detail"], result["result"])
    if not audit["all_passed"] or not evidence["all_passed"]:
        failed = [name for name, result in audit["checks"].items() if result["result"] != "PASS"]
        raise RuntimeError(f"audit failed: {failed}")
    logger.log("demo completed", f"run_id={run_id}; requirements={len(evidence['requirements'])}", "PASS")

    if backup.exists():
        shutil.rmtree(backup)
    if output.exists():
        os.replace(output, backup)
    os.replace(staging, output)
    if backup.exists():
        shutil.rmtree(backup)
    print(f"Artifacts written to {output}", flush=True)
    return 0
