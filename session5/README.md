# ERA V5 Session 5: V5 Mixture And Curriculum Plan

This is my proposed V5 mixture plan for a 40B India-first model trained over a
5T token-exposure budget. The numbers are written as a hypothesis to be tested
at 1B and 3B scale before any full-scale run trusts them.

The target model is not a code specialist with weak common sense. It should be
strong at coding, agentic tool use, controllable reasoning, long-context work,
and Indic language use, while still retaining the general web knowledge needed
to answer everyday Indian and global questions.

## 1. Budget By Capability Lane

| Capability lane | Share | Token exposures | Main datasets / inventory | Benchmarks it is meant to move | Supply risk |
|---|---:|---:|---|---|---|
| General web and common sense | 27% | 1.35T | FineWeb, DCLM, CulturaX, filtered Common Crawl, high-quality Wikipedia/news/forum slices | MMLU-Pro, MMMLU, broad chat quality | Low; abundant, but selector must reject boilerplate and spam |
| Code | 18% | 900B | Stack v2, permissive GitHub/repo data, programming docs, notebooks, competitive-programming traces | LiveCodeBench, HumanEval, Codeforces, SWE-bench coding subset | Medium; needs license filtering and dedup |
| STEM and knowledge | 12% | 600B | DCLM science, arXiv, textbooks, proofs, legal/technical documents, high-quality educational web | GPQA Diamond, MMLU-Pro, science/math evals | Medium; high-quality sources are smaller than raw web |
| Reasoning traces | 10% | 500B | AIME/GSM8K/MATH-style traces, proof traces, generated low/medium/high/ultra paired solutions | AIME, GSM8K, BigBench Extra Hard, HLE subset | High; must be generated and filtered heavily |
| Agentic and tool use | 10% | 500B | ToolBench, API/function-call traces, SWE-bench style repair traces, Codex/Claude/Cursor-like tool trajectories | Tau2, ToolBench, AgentBench, SWE-bench Verified | High; real long trajectories are scarce |
| Long context | 7% | 350B | Books, long legal docs, repo-scale tasks, multi-doc QA, long tool trajectories, long Indic documents | MRCR, needle retrieval, long-document QA, repo-level tasks | High; examples must be truly long, not chopped short |
| Indic protected slot | 8% | 400B | Sangraha, IndicCorp v2, CulturaX Indic, cleaned course shards, verified Indian-language public sources | IndicGenBench, FLORES-200, IndicXTREME, custom India-first eval | Very high; needs repetition and synthetic support |
| India-first civic/domain data | 3% | 150B | Indian law, policy, exams, public services, finance, education, agriculture, health, commerce, culture | Custom India-first eval, Indian public-service QA | Medium; broad but fragmented |
| Anneal/cooldown reserve | 5% | 250B | Best cleaned documents from every lane; no raw unverified data | Stability, final validation loss, all target evals | High quality only; intentionally held back |

The main tradeoff is that code, agentic, reasoning, and long-context together
take 45% of the run. I am not pushing them higher because the transcript was
clear that code without world knowledge becomes brittle. The 27% web lane is
there to preserve common sense and MMLU-style breadth.

## 2. Supply Accounting

The mixture is sized against the inventory instead of assuming every lane has
trillions of clean unique tokens.

| Lane | Target exposures | Plausible clean unique pool | How the target closes |
|---|---:|---:|---|
| General web/common sense | 1.35T | 2T+ | One pass from filtered web; no repetition pressure |
| Code | 900B | 600B-900B | License filter and repo dedup decide whether light repetition is needed |
| STEM/knowledge | 600B | 300B-500B | Repeat best documents 1.2-2x; generate some worked examples |
| Reasoning traces | 500B | 50B-150B | Cannot close from real data; needs distillation, verification, and repetition |
| Agentic/tool use | 500B | 20B-100B | Cannot close from public data; needs collected trajectories and synthetic tool tasks |
| Long context | 350B | 100B-250B | Needs document/repo preservation plus repetition of high-value long examples |
| Indic | 400B | 100B-150B native plus generated | Needs 2-3x repetition plus translated/synthetic tiers |
| India-first civic/domain | 150B | 50B-100B | Needs curation, translation into Indic languages, and QA generation |
| Anneal/cooldown | 250B | Held-out subset | Not extra supply; reserved best examples from all lanes |

The scarce lanes are deliberately smaller than the abundant web/code lanes even
though they matter more to the product target. Raising reasoning, agentic,
long-context, or Indic much above these numbers would require too much repeated
or generated data before proxy runs prove that it helps.

## 3. Indic Slot Split

The Indic lane is not a single headline number. Its 400B exposures are split by
trust tier:

| Indic tier | Share of Indic slot | Token exposures | Sources | Policy |
|---|---:|---:|---|---|
| Verified native | 45% | 180B | Sangraha verified, IndicCorp v2, CulturaX Indic after quality filtering, government/education/public-domain sources | Highest priority; can repeat up to 3x |
| Unverified native, cleaned | 20% | 80B | Sangraha unverified, raw Indic crawl, course-cleaned shards such as Sanskrit `unverified/san` | Allowed only after Session 4 style cleaning, PII scrub, language ID, dedup, decontamination |
| Translated | 15% | 60B | English STEM/code/public-service data translated into target Indic languages | Used for coverage gaps; always tagged as translated |
| Synthetic | 20% | 80B | Indic QA, summaries, explanations, reasoning traces, tool-use dialogs generated from verified seeds | Capped at 20% of Indic slot; no synthetic-only facts |

This closes the accounting problem honestly. Public native Indic supply is in
the tens of billions, not trillions. The 400B exposure target therefore requires
repetition and generation, but the highest-trust verified tier still dominates
the slot.

## 4. Protected Always-On Floor

The selector is not allowed to cross these floors in any batch:

| Protected lane | Minimum floor | Why the floor exists |
|---|---:|---|
| Indic | 8% | English/code-heavy proxy benchmarks would otherwise erase Indic capability |
| Agentic/tool traces | 4% | Tool traces look log-like and are easy for Opus-style filtering to discard |
| Reasoning traces | 3% | Reasoning control needs constant exposure before the late reasoning ramp |
| Long-context examples | 2% after 16k starts | Long-context skill cannot be learned from short chunks |
| India-first civic/domain | 1% | Preserves Indian policy, public-service, and cultural grounding |

Everything above the floor can still be selected by proxy loss, quality scores,
and curriculum stage. The floor is a guardrail against wishful benchmark
optimization, not a replacement for quality filtering.

## 5. Curriculum Schedule

The model should see every broad capability early, but depth and sequence
length should ramp gradually. Hard switches are avoided with 10-15% overlap
between neighboring phases.

| Phase | Training window | Sequence length | Mixture behavior |
|---|---:|---:|---|
| Foundation | 0-35% | 4k | Web-heavy; light code and STEM; Indic floor active from the first batch |
| Skill growth | 35-60% | 4k to 8k | Code and STEM rise; reasoning starts; agentic floor stays on |
| Specialist | 60-80% | 8k to 16k | Code, STEM, reasoning, and agentic lanes become dominant |
| Long-horizon | 80-95% | 16k to 32k/64k | Long context and multi-step tool trajectories ramp up |
| Anneal/cooldown | final 5% | mixed 8k to 64k | Best cleaned examples only; no noisy unverified data |

The anneal reserve is fixed at 5% of the full run, or 250B token exposures. It
is held back until the model is ready to absorb high-grade documents, reasoning
traces, code repairs, and long trajectories without wasting them.

## 6. Difficulty And Reasoning-Length Bands

Reasoning data must be tagged by required effort, not just by answer length.
The model should learn to spend short reasoning on easy tasks and long
reasoning only when the task warrants it.

| Band | Reasoning-token target | Example | Training target |
|---|---:|---|---|
| Instant | 0-64 | Estimate `43 / 17` | Direct answer or one mental step |
| Low | 64-256 | Count integers from 1 to 1000 divisible by 3 or 5 | Short inclusion-exclusion |
| Medium | 256-1k | Debug a single Python function from a traceback | Explain cause, patch, verify |
| High | 1k-4k | Solve an AIME-style algebra/number theory problem | Multi-step derivation with checks |
| Ultra | 4k-16k | Fix a multi-file repo issue with failing tests and tool calls | Plan, inspect, edit, run, recover, summarize |

For agentic traces, the model receives the full context but loss is applied
only to assistant decisions, assistant messages, and tool calls. Raw tool
observations, logs, compiler output, browser output, and API responses stay in
context but are not prediction targets.

## 7. Cleaning Priorities

Cleaning continues toward the cumulative data-gating target, but priority moves
to the starved lanes exposed by the mixture:

| Priority | Lane | Cleaning work |
|---|---|---|
| 1 | Indic verified/unverified | Script-aware normalization, language ID, quality scoring, PII scrub, dedup, provenance manifest |
| 2 | Agentic traces | Remove secrets, tag roles/tools/observations, mask loss on tool output, keep failure-recovery turns |
| 3 | Reasoning traces | Verify final answers, reject incoherent chains, tag effort band, decontaminate benchmark lookalikes |
| 4 | Long context | Preserve complete documents/repos, avoid cutting long examples into short unrelated chunks |
| 5 | Code | License filter, repo-level dedup, test/dependency metadata, remove generated/vendor noise |

The Session 4 Sanskrit shard is a useful proof that the pipeline can preserve
Brahmic-script data: it retained 31.03M of 31.12M tokens after eight cleaning
stages while recording language ID, PII, dedup, and provenance metadata.

## 8. Proxy Experiments Before Full Scale

This mixture is a hypothesis. It should not be trusted until cheap proxy runs
show that the extra budget buys the intended capability.

| Proxy | Variants | Confirmation metric | Refutation rule |
|---|---|---|---|
| 1B model | Proposed mix vs balanced baseline vs code-heavy ablation | Proposed mix improves Indic perplexity/FLORES, ToolBench-mini success, and HumanEval-mini while losing no more than 1% relative on MMLU-lite | If code-heavy wins coding with no general/Indic loss, move 2-3% from web to code; if Indic falls, raise verified native floor |
| 3B model | Proposed mix with long-context ramp vs same mix without ramp | MRCR/needle retrieval and long-document QA improve; SWE-bench-mini, Tau2 subset, AIME/GSM8K do not regress | If long-context metrics do not move, shift long-context tokens later and improve example construction |

The proxy harness should log per-lane validation loss, benchmark deltas, token
repetition rate, selector keep rate, and gradient/loss spikes at phase
transitions. A lane keeps its full-scale share only if its target benchmark
moves in the proxy run.

## 9. Acceptance Criteria

The plan is acceptable only if a reviewer can push on every number and trace it
back to a lane, dataset, benchmark, and supply constraint:

- All 100% of the 5T budget is assigned.
- The Indic slot is split across verified, unverified, translated, and
  synthetic tiers.
- Protected floors and anneal reserve are explicit.
- Agentic, reasoning, and long-context lanes are named directly.
- Difficulty and reasoning-length bands have real examples.
- Scarce lanes state where repetition or generation is needed.
- 1B and 3B proxy tests define metrics that can confirm or refute the mixture.
