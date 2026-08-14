# Session 7 Assignment — Reverse Kronecker Output Decoding

## Problem selected

This submission solves **Problem 5** from the assignment:

> Kronecker is deterministic in the forward direction. Can a model decode a
> token through a structured reverse path and avoid a vocabulary-sized final
> head?

The implemented proposal is **K-AR**, an autoregressive byte decoder conditioned
on the language model's hidden state.

## What the solution changes

A conventional language-model head learns one output row for every vocabulary
item:

```text
hidden state [d_model] → Linear(d_model, vocabulary) → token logits
```

K-AR instead predicts the token's UTF-8 serialization:

```text
hidden state → byte 1 → byte 2 → ... → EOS
```

Its output parameters depend on the 256-byte alphabet rather than vocabulary
size. The proof model compares:

1. a standard 10,000-way vocabulary head;
2. a parallel factorized byte decoder;
3. K-AR, the selected autoregressive byte decoder.

All three systems use the same Session 2 tokenizer, K32 input encoder,
Transformer body, multilingual data, initialization, and training budget.

## How the solution is proved

The evidence has two parts.

### 1. Projected-code reconstruction

The byte decoders receive projected K32 embeddings and reconstruct held-out
complete token forms. Controlled noise tests measure whether decoding remains
stable when the input is only approximately on a valid code.

### 2. Multilingual next-token modeling

A two-layer causal Transformer is trained on balanced English, Hindi, Telugu,
and Kannada data. The output heads are compared on:

- token negative log-likelihood and bits per UTF-8 byte;
- exact decoded next-token accuracy;
- valid UTF-8 and known-vocabulary rates;
- performance by language and byte length;
- output parameters and peak logits tensor memory;
- training throughput and greedy decoding latency;
- three-seed variance in the full profile.

This separates exact codec inversion from the harder language-model problem in
which a hidden state represents uncertainty over several plausible next tokens.

## Reproduce

Run from the repository root:

```bash
python3 -m pytest session7/tests

# Fast end-to-end validation
python3 -m session7.run_all all --profile smoke --no-checkpoints

# CPU-rigorous assignment run
python3 -m session7.run_all analyze --profile full
python3 -m session7.run_all reconstruct --profile full
python3 -m session7.run_all lm --profile full
python3 -m session7.run_all report --profile full
```

The report is written to `session7/report/index.html`. It is self-contained and
can be opened directly or served by any static web server.

## Full-profile result

The experiment was completed with configuration fingerprint
`d8dfc772972ced04`: two learning-rate pilots per head followed by three seeds at
1,000,000 training tokens per architecture and seed. All heads selected a
learning rate of `1e-3`.

| Architecture | Head parameters | Validation token NLL | Test greedy exact | Test beam exact | Valid UTF-8 | Peak logits | Greedy latency |
|---|---:|---:|---:|---:|---:|---:|---:|
| Vocabulary head | 1,290,000 | 8.221 ± 0.217 | 2.073% | 2.865% | 100.0% | 78.13 MiB | 0.008 ms/token |
| Parallel byte | 66,177 | 19.255 ± 0.140 | 0.052% | 0.000% | 36.7% | 21.25 MiB | 0.049 ms/token |
| **K-AR** | **140,673** | **12.557 ± 0.121** | **0.375%** | **2.083%** | **78.2%** | **21.25 MiB** | **0.390 ms/token** |

The result is a **partial success and a useful negative finding**:

- K-AR removes the vocabulary-sized head: it is 9.17× smaller than the
  standard head, while the complete model is 41.8% smaller.
- K-AR is materially better than the parallel byte control on NLL, exact
  generation, beam accuracy, and UTF-8 validity. Modeling dependencies between
  bytes matters.
- K-AR beam exact accuracy reaches 2.083%, compared with 2.865% for the
  vocabulary head. Greedy accuracy remains within the declared three-point
  tolerance, although that loose criterion should not be confused with parity.
- K-AR does **not** satisfy the quality contract: its validation NLL is 52.7%
  higher and only 78.2% of greedy outputs are valid UTF-8.
- Peak logits memory improves 3.68×, missing the 4× target, and greedy K-AR
  decoding is about 47× slower than the vocabulary head on this CPU benchmark.
- Held-out projected-code reconstruction is also not solved: clean exact
  recovery is 4.40% overall and 4.54% for ≤32-byte forms. A stored codebook
  cosine lookup reaches 98.95%, showing that the projection retains almost all
  identity information but a compact learned inverse does not recover it with
  this training protocol.

Therefore the assignment **does solve the investigation of Problem 5**: it
implements the proposed inverse, tests it against controlled baselines, and
shows exactly which claims hold. It does **not** prove that K-AR is ready to
replace a production vocabulary head. The best next experiment is constrained
UTF-8-aware decoding or byte-trie decoding, followed by distillation from the
vocabulary head; both target the measured validity and NLL failures without
changing the shared K32 input experiment.

## Experimental defaults

| Setting | Value |
|---|---:|
| Vocabulary | 10,000 tokens |
| Languages | English, Hindi, Telugu, Kannada |
| K32 input | 32 positions × 256 bytes |
| Model width | 128 |
| Transformer | 2 layers, 4 heads, FFN 512 |
| Context | 128 tokens |
| Full training | 1,000,000 tokens per architecture and seed |
| Seeds | 7, 17, 29 |
| Output limit | 128 bytes plus EOS |

Tokens above 32 bytes remain in the dataset and use the original identical K32
input behavior in every model. A separate ≤32-byte metric isolates output-head
quality from that shared input limitation. Problem 3/K32-O is deliberately not
mixed into this assignment.

## Success contract

The core proposal is considered successful only if it achieves:

- at least 8× fewer output parameters;
- at least 4× lower peak output-logit tensor memory;
- at least 99% exact clean reconstruction on supported held-out K32 forms;
- at least 99% valid UTF-8 on natural-language test outputs;
- validation token NLL within 10% of the vocabulary-head baseline;
- greedy exact next-token accuracy within three absolute percentage points;
- consistent full-profile results across three seeds.

Greedy p95 latency within 5× of the vocabulary head is a separate
deployment-grade target. A slower decoder can prove compression without proving
deployment superiority.

## Scope and honest limitations

- The decoder replaces a large dense head with a smaller structured module; it
  does not make decoding free.
- Generating an unseen byte string does not mean the model knows facts about it.
- The current tokenizer still defines the training sequence. Fully dynamic
  insertion of generated out-of-vocabulary strings is not claimed.
- A 10,000-token CPU experiment is evidence about the mechanism, not proof of
  production-scale superiority.
- All failures and downgrade criteria are retained in
  `PROBLEM_ANALYSIS_AND_PROPOSAL.md`.

## Files

```text
session7/
├── README.md
├── PROBLEM_ANALYSIS_AND_PROPOSAL.md
├── run_all.py
├── src/                 # codec, heads, model, training, and evaluation
├── tests/               # invariants and end-to-end smoke tests
├── artifacts/           # generated JSON evidence and optional checkpoints
└── report/index.html    # generated self-contained evidence report
```
