"""Backward-compatible facade for the modular :mod:`v5` package.

New integrations should import from the owning subsystem module. This facade
keeps the original public names available for notebooks and tests created
before the implementation was split.
"""

from v5.audit import audit_artifacts, generate_evidence
from v5.common import (
    CRASH_EXIT_CODE,
    GENESIS_HASH,
    ROOT,
    SCHEMA_VERSION,
    RunLogger,
    canonical_bytes,
    configure_determinism,
    hash_file,
    read_json,
    read_jsonl,
    sha256_bytes,
    sha256_json,
    tensor_state_hash,
    write_json,
    write_jsonl,
)
from v5.data import ByteTokenizer, build_shards, clean_text, load_documents, tokenize_document, validate_manifests
from v5.demo import run_demo
from v5.interfaces import (
    CheckpointStoreProtocol,
    CurriculumStage,
    LedgerStoreProtocol,
    PackingPolicyProtocol,
    SampleSelectorProtocol,
    TokenizerProtocol,
)
from v5.model import TinyCausalLM, make_model, state_dict_cpu
from v5.pipeline import (
    DEFAULT_PACKING_POLICIES,
    LOSS_BEARING_ROLES,
    PROTECTED_LANES,
    GradientAlignmentSelector,
    PackingPolicyRegistry,
    assert_train_rows,
    build_batches,
    build_packed_sequence,
    chunk_row,
    compile_lane_schedule,
    make_batch,
    pack_rows,
    score_opus,
    sequence_tensors,
)
from v5.recovery import build_performance_report, create_fork, evaluate_firewalled_splits, replay_history
from v5.training import (
    JsonlHashChainLedger,
    LocalCheckpointStore,
    batch_tensors,
    load_batch,
    load_checkpoint,
    optimizer_and_scheduler,
    save_checkpoint,
    train_batch,
    training_worker,
    verify_hash_chain,
    write_ledger_projections,
)

__all__ = [name for name in globals() if not name.startswith("_")]
