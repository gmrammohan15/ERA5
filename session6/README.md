# V5 Training Data Execution System

This repository is a small, complete proof that a language-model training data
stream can be made reproducible, resumable, replayable, and auditable. It uses
a bundled multilingual corpus and a tiny real causal Transformer; scale and
model quality are deliberately out of scope.

## Run the complete demonstration

```bash
python -m pip install -r requirements.txt
python run_demo.py
```

The second command performs the entire demonstration without network access or
manual intervention. It replaces `submission_artifacts/` only after a new run
passes its independent audit. A normal CPU run is intended to finish in under
two minutes.

## Architecture

```text
bundled documents
  -> frozen UTF-8 byte tokenizer
  -> content-addressed immutable JSONL shards + manifests
  -> three-stage lane schedule + protected floors
  -> gradient-alignment OPUS decisions
  -> data-type-specific fixed-length packing
  -> deterministic tiny Transformer training
  -> hash-chained consumption + learning records
  -> checkpoint -> child-process crash -> fresh-process resume
  -> ledger-driven replay -> earlier-checkpoint fork -> audit/evidence
```

The byte tokenizer has only PAD, BOS, EOS, and the 256 possible UTF-8 bytes. It
is compact, frozen, lossless for Indic text and code, and needs no downloaded
model. Shard filenames are content addressed; manifests bind content to the
tokenizer and cleaning policy hashes. Readers validate those hashes before
using a shard.

The curriculum has foundation, skill-growth, and anneal stages over web, code,
reasoning, agentic, and Indic lanes. Indic, agentic, and reasoning appear in
every global batch through protected floors. OPUS uses real candidate-prefix
gradients and a selection-proxy gradient. Its original decision is retained
when the floor controller overrides a rejection or deferral.

Packing is chosen by data type: best-fit for prose/Indic data, greedy for code
and reasoning, and structure-preserving for agent traces. Every packed sequence
stores labels, loss masks, block-causal attention masks, reset position IDs,
and source token spans. Agent prompts and tool observations provide context but
do not bear loss.

Training uses an actual one-block Transformer. The authoritative step ledger is
append-only and SHA-256 chained; consumption and learning ledgers are
verifiable projections. Learning records contain per-token and per-sample
cross-entropy, gradient norm, learning rate, source location, and model-state
hashes.

The orchestrator launches a child trainer, saves a checkpoint after four
committed batches, records the exact next batch, and terminates the child with
exit code 86 before that batch trains. A fresh child restores model, optimizer,
scheduler, RNG, data cursor, and ledger head, then proves its first batch is the
expected one. Replay rebuilds an earlier interval from ledger spans rather than
rerunning selection. A separate code-heavy branch starts from the earlier
checkpoint and records parent lineage.

## Evidence and tests

The generated directory contains the required `run.log`, `evidence.json`,
`evidence.md`, `performance.json`, manifests, ledgers, and checkpoints, plus
the immutable shards, packed batches, replay report, and fork artifacts.
Evidence PASS/FAIL values are rendered from an auditor that reopens artifacts
and recomputes hashes, masks, schedules, ledger chains, recovery, replay, and
performance arithmetic.

Run the automated invariant suite with:

```bash
python -m pytest -q
```

`run_demo.py` remains the single entry point. The reusable implementation lives
in the `v5/` package:

- `data.py` owns the tokenizer, cleaning, shards, and manifests.
- `curriculum.py`, `selection.py`, `packing.py`, and `batches.py` own the
  schedule/floors, OPUS/firewall, packing/masks, and global-batch contracts.
- `training.py` owns the trainer, hash-chain ledger backend, and local
  checkpoint backend.
- `recovery.py` owns replay, resume-related reconstruction, fork, evaluation,
  and performance reporting.
- `audit.py` independently verifies artifacts and generates evidence.
- `demo.py` is the orchestration layer used by the CLI.

`interfaces.py` defines extension contracts for tokenizers, packing policies,
sample selectors, ledgers, and checkpoint stores. `v5_system.py` is now only a
backward-compatible import facade; `pipeline.py` similarly preserves older
pipeline imports. The agreed detailed design is preserved in
`IMPLEMENTATION_PLAN.md`.
