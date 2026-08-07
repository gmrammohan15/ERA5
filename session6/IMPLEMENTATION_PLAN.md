# V5 Training Data Execution System — Implementation Plan

Build a self-contained, CPU-only Python system that demonstrates the complete
training-data path:

```text
documents -> frozen tokenization -> immutable shards/manifests
-> curriculum and OPUS selection -> packed global batches
-> real model training -> consumption/learning ledgers
-> checkpoint -> subprocess crash -> exact resume
-> historical replay -> checkpoint fork -> independent audit
```

The repository will use a bundled multilingual toy corpus, a frozen byte-level
tokenizer, content-addressed shards, three curriculum stages, protected Indic,
agentic and reasoning floors, real gradient-alignment OPUS scoring, data-type
specific packing, and a deterministic tiny causal Transformer.

`python run_demo.py` will rebuild `submission_artifacts/`, launch a child
trainer that deliberately exits after a checkpoint, resume in a fresh process,
verify the exact next batch, replay an earlier interval, fork an earlier
checkpoint, generate performance measurements, run an independent audit, and
produce `evidence.json` and `evidence.md` from the audit results.

The authoritative training ledger will be append-only and hash-chained. It
will link every optimizer update to source shard rows and token spans, OPUS
decisions, packed tensor hashes, per-token/sample loss, gradient norm, and model
state hashes. Checkpoints will contain model, optimizer, scheduler, RNG, loader
cursor, and ledger head state.

Automated tests will cover tokenizer and manifest integrity, firewall behavior,
packing masks and positions, protected floors, OPUS outcomes, ledger tamper
detection, checkpoint restoration, subprocess resume, replay, fork lineage,
and evidence/performance reconstruction.

Assumptions: Python 3.10+, PyTorch CPU, no network or external data, sequence
length 64, global batch size 8, 12 main optimizer steps, and a target runtime
below two minutes on a normal CPU.

## Implemented package boundaries

The reusable implementation is split by responsibility under `v5/`:

```text
common -> data/model -> curriculum/selection/packing/batches
       -> training -> recovery -> audit -> demo orchestration
```

Curriculum stages remain configuration records. Extension protocols cover
tokenizers, packing-policy registries, sample selectors, ledger backends, and
checkpoint stores. `run_demo.py` remains the only execution entry point;
`v5_system.py` and `v5.pipeline` are compatibility facades rather than owners
of implementation logic.
