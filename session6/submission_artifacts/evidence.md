# V5 Execution Evidence

| Requirement | Result | Evidence |
|---|---|---|
| Tokenizer integrity | PASS | manifests/shard_index.json, manifests/tokenizer.manifest.json, shards/ |
| Evaluation firewall | PASS | ledgers/consumption.jsonl, ledgers/evaluation.jsonl, ledgers/firewall_report.json |
| Packing correctness | PASS | batches/, performance/packing_report.json |
| Mixture compliance | PASS | batches/, ledgers/consumption.jsonl, manifests/mixture_schedule.json |
| OPUS audit trail | PASS | ledgers/opus_decisions.jsonl |
| Crash recovery | PASS | checkpoints/crash_intent.json, ledgers/step_ledger.jsonl, run.log |
| Replay | PASS | replay/replay_report.json |
| Learning trace | PASS | ledgers/learning.jsonl, ledgers/step_ledger.jsonl |
| Throughput | PASS | ledgers/step_ledger.jsonl, performance.json |

Overall result: **PASS**
