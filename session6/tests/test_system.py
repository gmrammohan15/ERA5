from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from v5_system import (
    ByteTokenizer,
    GENESIS_HASH,
    ROOT,
    assert_train_rows,
    build_packed_sequence,
    compile_lane_schedule,
    sha256_json,
    verify_hash_chain,
)
from v5.interfaces import CurriculumStage, LedgerStoreProtocol, PackingPolicyProtocol, TokenizerProtocol
from v5.pipeline import PackingPolicyRegistry
from v5.training import JsonlHashChainLedger, LocalCheckpointStore


@pytest.fixture()
def tokenizer() -> ByteTokenizer:
    with (ROOT / "config" / "tokenizer.json").open(encoding="utf-8") as handle:
        return ByteTokenizer(json.load(handle))


def test_byte_tokenizer_is_faithful_and_stable(tokenizer: ByteTokenizer) -> None:
    samples = ["India", "भारत", "తెలుగు", "ಕನ್ನಡ", "def f(x):\n    return x + 1"]
    assert all(tokenizer.decode(tokenizer.encode(sample)) == sample for sample in samples)
    assert tokenizer.tokenizer_hash == sha256_json(tokenizer.config)
    assert tokenizer.vocab_size == 259


def test_packing_masks_roles_boundaries_and_positions(tokenizer: ByteTokenizer) -> None:
    segments = [
        {
            "tokens": tokenizer.encode("Q:A"),
            "roles": ["user", "assistant", "assistant"],
            "ref": {"shard_id": "train-agentic-x", "row_id": 0, "doc_id": "a", "token_start": 0, "token_end": 3, "span_hash": sha256_json(tokenizer.encode("Q:A"))},
        },
        {
            "tokens": tokenizer.encode("ok"),
            "roles": ["content", "content"],
            "ref": {"shard_id": "train-agentic-x", "row_id": 1, "doc_id": "b", "token_start": 0, "token_end": 2, "span_hash": sha256_json(tokenizer.encode("ok"))},
        },
    ]
    sequence = build_packed_sequence(segments, "agentic", "test", tokenizer, 16)
    assert len(sequence["input_ids"]) == 16
    assert sequence["position_ids"][0] == 0
    second_start = sequence["source_spans"][1]["packed_start"]
    assert sequence["position_ids"][second_start] == 0
    assert sequence["loss_mask"][0] == 0  # BOS predicts a user token.
    boundary_query = second_start - 1
    assert sequence["loss_mask"][boundary_query] == 0
    assert not sequence["attention_mask"][second_start][0]
    assert all(not sequence["attention_mask"][query][key] for query in range(16) for key in range(query + 1, 16))
    for index, role in enumerate(sequence["token_roles"][:-1]):
        if role == "pad":
            assert sequence["loss_mask"][index] == 0


def test_schedule_honors_every_protected_floor() -> None:
    with (ROOT / "config" / "demo.json").open(encoding="utf-8") as handle:
        config = json.load(handle)
    _, by_stage, report = compile_lane_schedule(config)
    for stage in report["stages"]:
        for lanes in by_stage[stage["stage"]]:
            assert lanes.count("indic") >= 1
            assert lanes.count("agentic") >= 1
            assert lanes.count("reasoning") >= 1
        assert sum(stage["actual_sequence_counts"].values()) == config["global_batch_size"] * config["steps_per_stage"]


def test_firewall_rejects_every_non_train_split() -> None:
    for split in ("eval", "validation", "selection_proxy"):
        with pytest.raises(PermissionError):
            assert_train_rows([{"doc_id": split, "split": split}], "test")
    assert_train_rows([{"doc_id": "train", "split": "train"}], "test")


def test_hash_chain_detects_tampering() -> None:
    first_core = {"previous_hash": GENESIS_HASH, "value": 1}
    first = {**first_core, "record_hash": sha256_json(first_core)}
    second_core = {"previous_hash": first["record_hash"], "value": 2}
    second = {**second_core, "record_hash": sha256_json(second_core)}
    assert verify_hash_chain([first, second])[0]
    tampered = copy.deepcopy([first, second])
    tampered[0]["value"] = 99
    assert not verify_hash_chain(tampered)[0]


def test_reusable_interfaces_and_data_driven_stages(tokenizer: ByteTokenizer, tmp_path: Path) -> None:
    stage = CurriculumStage.from_mapping(
        {"name": "custom", "index": 7, "weights": {"general_web": 0.25, "code": 0.75}}
    )
    assert stage.name == "custom" and stage.weights["code"] == 0.75
    assert isinstance(tokenizer, TokenizerProtocol)

    policies = PackingPolicyRegistry()
    assert isinstance(policies, PackingPolicyProtocol)
    policies.register("code", "structure_preserving")
    assert policies.policy_for("code") == "structure_preserving"

    ledger = JsonlHashChainLedger(tmp_path / "steps.jsonl")
    assert isinstance(ledger, LedgerStoreProtocol)
    core = {"previous_hash": GENESIS_HASH, "value": "extensible"}
    ledger.append({**core, "record_hash": sha256_json(core)})
    assert ledger.verify()[0]


def test_local_checkpoint_backend_roundtrip(tmp_path: Path) -> None:
    store = LocalCheckpointStore(tmp_path)
    path = store.save("adapter_test", {"next_batch_index": 9, "payload": [1, 2, 3]})
    restored = store.load(path)
    assert restored["next_batch_index"] == 9
    assert restored["payload"] == [1, 2, 3]


def test_generated_bundle_if_present() -> None:
    artifacts = ROOT / "submission_artifacts"
    if not artifacts.exists():
        pytest.skip("run python run_demo.py to generate the integration bundle")
    evidence = json.loads((artifacts / "evidence.json").read_text(encoding="utf-8"))
    assert evidence["all_passed"]
    assert all(item["result"] == "PASS" for item in evidence["requirements"].values())
    run_log = (artifacts / "run.log").read_text(encoding="utf-8")
    for marker in (
        "[PASS] tokenizer_hash_verified",
        "[PASS] eval_shard_blocked",
        "[PASS] checkpoint_saved",
        "[PASS] resume_next_batch_matched",
        "[PASS] replay_hash_matched",
    ):
        assert marker in run_log


def test_generated_opus_and_protected_override_if_present() -> None:
    artifacts = ROOT / "submission_artifacts"
    if not artifacts.exists():
        pytest.skip("run python run_demo.py to generate the integration bundle")
    records = [json.loads(line) for line in (artifacts / "ledgers" / "opus_decisions.jsonl").read_text(encoding="utf-8").splitlines()]
    assert {"accepted", "rejected", "deferred"}.issubset({record["base_decision"] for record in records})
    assert any(record["protected_floor_override"] for record in records)
    assert all(record["model_state_hash"] for record in records)


def test_generated_recovery_replay_and_fork_if_present() -> None:
    artifacts = ROOT / "submission_artifacts"
    if not artifacts.exists():
        pytest.skip("run python run_demo.py to generate the integration bundle")
    intent = json.loads((artifacts / "checkpoints" / "crash_intent.json").read_text(encoding="utf-8"))
    steps = [json.loads(line) for line in (artifacts / "ledgers" / "step_ledger.jsonl").read_text(encoding="utf-8").splitlines()]
    resumed = steps[intent["expected_batch_index"]]
    assert resumed["consumption"]["batch_id"] == intent["expected_batch_id"]
    assert [record["global_step"] for record in steps] == list(range(12))
    replay = json.loads((artifacts / "replay" / "replay_report.json").read_text(encoding="utf-8"))
    assert replay["all_matched"]
    fork = json.loads((artifacts / "branches" / "fork_code_heavy" / "fork_report.json").read_text(encoding="utf-8"))
    assert fork["initial_model_hash_matched"] and fork["branch_diverged"] and fork["branch_ledger_chain_valid"]
