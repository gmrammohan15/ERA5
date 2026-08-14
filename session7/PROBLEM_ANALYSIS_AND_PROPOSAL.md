# Session 7: Problem Analysis and Proposal

## Purpose

Session 7 asks us to choose one extension to Kronecker Embeddings, explain the
solution, and provide code and evidence showing whether it works. This document
records all five candidate problems, evaluates them, and selects Problem 5:
replacing the vocabulary-sized output head with a structured reverse decoder.

The principal references are:

- `Session7_Transcript.md`, especially the Kronecker discussion beginning near
  01:45:00 and the assignment beginning near 02:25:00.
- `assignment.md`.
- *Kronecker Embeddings: Byte-Level Structured Token Representations for
  Parameter-Efficient Language Models*, arXiv:2605.29459.

## Kronecker background

A conventional input embedding stores a learned table

\[
E\in\mathbb{R}^{|V|\times d_{\text{model}}}.
\]

Kronecker replaces that table with a fixed byte-position codec and one learned
projection. For a token containing UTF-8 bytes \(b_1,\ldots,b_L\),

\[
\kappa(b)=\frac{1}{\sqrt{L}}\sum_{p=1}^{L}c_{b_p}\otimes p_p,
\]

where \(c_{b_p}\) is a 256-way byte one-hot vector and \(p_p\) is a position
one-hot vector. With 256 byte values and 32 positions,

\[
D=256\times32=8192.
\]

The model input is

\[
z=\kappa(b)W_{\text{proj}},
\qquad
W_{\text{proj}}\in\mathbb{R}^{8192\times d_{\text{model}}}.
\]

The byte-position codec is fixed; only the projection is trained. Within the
32-byte window, distinct positions occupy orthogonal coordinate blocks.

The number 32 therefore is not an incidental implementation constant. It is
one factor of the Kronecker codec and determines its width, parameter count,
geometry, and maximum represented byte position.

## Candidate Problem 1: embeddings with mathematical structure

### Problem statement

Can an embedding contain explicit mathematical structure so that operations on
embeddings reflect operations on the represented values? For example, can the
representation of \(9\) combined with itself under addition yield the
representation of \(18\), and under multiplication yield the representation of
\(81\)?

### Strongest viable direction

Use a protected arithmetic side channel alongside the lexical Kronecker
representation:

\[
E(t)=[K_{\text{UTF8}}(t);A(n)].
\]

For integers, one simple exact additive representation is

\[
A(n)=nu.
\]

Then

\[
A(a)+A(b)=A(a+b).
\]

Multiplication cannot generally be obtained from ordinary vector addition. It
requires a separate bilinear operator, for example:

\[
C_\times(x,y)=u(w^\top x)(w^\top y),
\qquad w^\top u=1.
\]

This gives \(C_\times(A(a),A(b))=A(ab)\).

### Advantages

- Strong algebraic proof is possible.
- CPU-scale experiments are straightforward.
- Out-of-range arithmetic generalization can be measured cleanly.
- The representation can be appended to the existing lexical representation.

### Limitations

- This is close to supplying an internal calculator rather than proving that a
  model discovered mathematical meaning.
- Exact addition and multiplication require different operators.
- Finite-precision vectors cannot represent every integer exactly.
- Layer normalization or arbitrary learned projections can corrupt a protected
  arithmetic channel.
- Closely related ideas already exist in neural arithmetic units, scalar-value
  embeddings, residue encodings, and Fourier number encodings.

### Assessment

This is the easiest problem to prove rigorously, but its novelty and breadth of
impact are limited unless the work discovers a more general compositional
algebra rather than installing hand-written arithmetic.

## Candidate Problem 2: one Kronecker framework for text, images, and audio

### Problem statement

Can the Kronecker idea be extended to text, image patches, and audio patches so
that all three modalities enter a model through one structured embedding
interface?

### Strongest viable direction

Represent every patch as typed value-coordinate events:

\[
e_i=(v_i,q_{i1},q_{i2},c_i,\tau_i),
\]

then bind value, coordinates, channel, and type:

\[
\kappa(P)=S\left[
\sum_{i\in P}
\phi(v_i)\otimes r_1(q_{i1})\otimes r_2(q_{i2})
\otimes r_c(c_i)\otimes r_\tau(\tau_i)
\right].
\]

Here \(S\) is a fixed sketch that avoids materializing the full tensor product.
One learned projection maps the fixed sketch to model width.

### Advantages

- A single conceptual input interface for multiple modalities.
- Explicit value-position binding generalizes Kronecker naturally.
- Parameter sharing and zero-new-parameter modality onboarding are potentially
  useful.

### Limitations

- Image and audio values have neighborhood structure; UTF-8 byte identities do
  not. A single value geometry may be inappropriate.
- Patch embedding parameters are already relatively small compared with text
  vocabulary tables.
- A meaningful proof requires multiple datasets, preprocessing pipelines, and
  modality-specific baselines.
- Tensor-product representations, patch projections, TensorSketch, Perceiver,
  ByteFormer, and multimodal shared encoders provide substantial prior art.

### Assessment

This has good potential impact but too broad an experimental surface for the
current assignment. A toy digit experiment would be feasible but would not
justify a broad multimodal claim.

## Candidate Problem 3: remove the fixed 32-byte limit

### Problem statement

The original codec has 32 byte-position slots. Short tokens use only a subset,
while tokens longer than 32 UTF-8 bytes are truncated. Can Kronecker support
long tokens dynamically without forcing a wider codec for every token?

### Important clarification

The limit is 32 UTF-8 **bytes**, not 32 bits and not necessarily 32 Unicode
characters. An ASCII character usually occupies one byte, while an Indic
codepoint commonly occupies three bytes and a grapheme cluster may contain
multiple codepoints.

The apparent short-token waste is also smaller than it first appears. For a
five-byte token, unused positions contribute zero. An on-the-fly implementation
can gather and sum only the five active byte-position rows. It does not need to
construct 27 padded events. The fixed projection still contains parameters for
all 32 positions, but those parameters are shared across the entire vocabulary.

The real correctness issue is truncation after 32 bytes. The paper reports a
low aggregate truncation rate across its tested tokenizers, but this must be
remeasured on the Indic-heavy tokenizer and corpus used here. A low frequency
does not imply low impact if affected tokens are systematically multilingual,
technical, or identifier-like.

### Why simply making the codec dynamic is unsafe

A linear projection requires a fixed input width. If the position dimension
changes with token length, the projection shape changes too:

\[
W_L\in\mathbb{R}^{(256L)\times d_{\text{model}}}.
\]

Using a different projection for every length defeats parameter sharing.
Increasing the global limit from 32 to 64 instead changes the codec width from
8192 to 16384 and doubles projection parameters.

Compressing an arbitrary sequence into one fixed-width vector introduces other
losses:

- globally orthogonal byte-position coordinates are lost;
- exact pre-projection reconstruction is lost;
- the original byte-at-the-same-position similarity interpretation changes;
- recurrent or attention-based composition introduces more trainable
  parameters and computation;
- variable-length composition is harder to batch efficiently;
- one finite-precision fixed-width vector cannot be collision-free for
  unbounded strings.

For these reasons, the proposal should preserve K32 rather than replacing it.

## Candidate Problem 4: a Fourier alternative

### Problem statement

Can each character be represented as a Fourier wave and can the character waves
be combined to form a structured word embedding?

### Strongest viable direction

Bind character identity to positional phase:

\[
U_k(x)=\frac{1}{\sqrt{L}}
\sum_{i=0}^{L-1}a_k(c_i)e^{i\omega_ki}.
\]

An additional directed transition spectrum can encode adjacent order:

\[
T_k(x)=\frac{1}{\sqrt{L-1}}
\sum_{i=0}^{L-2}
a_k(c_i)\overline{a_k(c_{i+1})}e^{i\omega_ki}.
\]

### Advantages

- Deterministic and streamable.
- Position shifts have a clean Fourier interpretation.
- Complex phase binding can distinguish permutations when position is included.
- Fourier operations are well supported computationally.

### Limitations

- Summing character waves without position is permutation invariant.
- With positional phase, recovery noise grows with string length.
- A fixed number of Fourier coefficients cannot robustly encode arbitrary
  strings.
- A full invertible DFT requires a number of coefficients proportional to
  length, eliminating fixed-width compression.
- Holographic reduced representations, Fourier binding, and complex positional
  word encodings are established prior art.

### Assessment

This is mathematically attractive but high risk. It is likely to produce
interesting visualizations while providing a weaker practical result than a
carefully extended Kronecker codec.

## Candidate Problem 5: reverse deterministic embeddings and remove the head

### Problem statement

Can a model output be decoded back into the token that produced a deterministic
Kronecker representation, allowing a large or open vocabulary without a
vocabulary-sized output head?

### Key distinction

The fixed K32 codec is reversible before projection within its supported window:
each byte-position coordinate can be inspected. This does not imply that an LM
hidden state is reversible. During language modeling, the hidden state encodes
a conditional distribution over plausible next tokens. At initialization it is
not close to any valid token code, and even a trained model may need to represent
multiple possible continuations.

Nearest-neighbor decoding therefore confuses exact codec inversion with
probabilistic language modeling.

### Strongest viable direction

Use a structured byte decoder:

- a fast parallel byte-position categorical decoder;
- an explicit end-of-token or length distribution;
- a small autoregressive byte decoder when the parallel decoder is uncertain;
- categorical cross-entropy or KL divergence rather than direct vector
  regression;
- optional contrastive loss and hidden-state noise training.

### Advantages

- Could genuinely remove the \(d_{\text{model}}\times |V|\) parameter matrix.
- Can generate unseen byte strings.
- Potentially large deployment-memory impact.

### Limitations

- It replaces the vocabulary head with another output module; it does not make
  output decoding free.
- Independent byte positions can combine parts of different likely words into
  invalid strings.
- Autoregressive local decoding adds serial inference latency.
- A large vocabulary does not give the model knowledge of all its entries.
- Continuous-output, error-correcting-output-code, compositional-output, and
  byte-level language models already cover much of the design space.

### Assessment

This has the highest potential impact and was identified in the session as the
most relevant problem. It is also the most difficult to prove fairly. It is a
strong follow-up project after a successful input-side extension.

# Impact Review and Selected Direction

## What each problem would solve

| Problem | What it solves | Practical impact | Main risk |
|---|---|---|---|
| 1. Mathematical structure | Gives numbers an explicit arithmetic representation so operations can generalize beyond memorized examples. | Better arithmetic, quantity, and symbolic reasoning. | May amount to installing a calculator rather than learning mathematical meaning. |
| 2. Multimodal Kronecker | Creates one value-position interface for text, image patches, and audio patches. | Shared multimodal architecture and easier modality onboarding. | Very broad proof surface; non-text patch embeddings are already relatively small. |
| 3. Dynamic length | Prevents tokens above 32 UTF-8 bytes from losing suffix information. | Better multilingual, technical-term, URL, and identifier robustness. | The affected real token mass may be too small to justify added complexity. |
| 4. Fourier alternative | Replaces explicit position-byte blocks with streamable frequency and phase binding. | Potentially elegant and length-friendly structured encoding. | Collision, recovery, and prior-art risk; a full invertible transform grows with length. |
| 5. Reverse Kronecker | Predicts token bytes without a vocabulary-sized output matrix. | Can remove billions of output parameters and support generated strings outside a fixed vocabulary. | Hard probabilistic decoding problem; output generation becomes serial or structured. |

## Top two by impact

### Rank 1: Problem 5 — reverse deterministic Kronecker

Problem 5 has the highest raw impact. Removing the input embedding table solves
only one side of the model interface. A conventional model still pays for a

\[
W_{\text{head}}\in\mathbb{R}^{d_{\text{model}}\times |V|}
\]

output matrix. At a vocabulary of one million and model width 8192, that matrix
alone contains 8.192 billion parameters. A decoder whose parameters depend on
the 256-byte alphabet rather than \(|V|\) changes the economics of large and
open vocabularies.

The difficulty is equally large. A language-model hidden state represents a
distribution over plausible next tokens, not one exact K32 point. The research
claim must therefore be about a compact probabilistic structured output model,
not simple nearest-neighbor inversion.

### Rank 2: Problem 3 — dynamic K32 overflow

Problem 3 has the best combination of practical impact and proof feasibility.
The local vocabulary contains 300 tokens above 32 UTF-8 bytes, and observed
over-32 token mass is approximately 0.58% English, 1.00% Hindi, 1.96% Telugu,
and 1.22% Kannada. A conditional overflow path can preserve exact K32 behavior
for common tokens while fixing a real multilingual and identifier-like edge
case.

Problem 3 remains a strong follow-up, but it does not remove the dominant
large-vocabulary output matrix. Problem 5 is therefore selected for the current
assignment.

## Selected research question

> Can a small language model replace a vocabulary-sized output head with an
> autoregressive byte decoder, substantially reduce output parameters and
> output-layer memory, and retain competitive multilingual next-token quality?

## Selected solution: K-AR — Kronecker Autoregressive Reverse Decoder

All compared systems share the same tokenizer, K32 input encoder, Transformer
body, data order, and training budget. Only the output mechanism changes.

The selected decoder models a token byte string

\[
y=(b_1,\ldots,b_L,\mathrm{EOS})
\]

conditioned on the Transformer state \(h\):

\[
p(y\mid h)=\prod_{i=1}^{L+1}p(y_i\mid y_{<i},h).
\]

It uses:

- a 64-dimensional previous-byte embedding;
- one GRU layer of width 128;
- an initial hidden state projected from the Transformer output;
- 257 output classes: 256 byte values plus EOS;
- teacher forcing in training and greedy or beam decoding in evaluation.

Its output parameter count is independent of vocabulary size. For the local
10,000-token proof model at width 128, the conventional head has approximately
1.29 million parameters while K-AR has approximately 141 thousand, a reduction
of about nine times.

## Baselines

1. A standard \(128\times10{,}000\) vocabulary head.
2. A factorized parallel byte-position decoder using a shared byte classifier.
3. K-AR, the selected autoregressive byte decoder.

The parallel decoder tests whether serial dependence is necessary. It is
faster, but independent byte positions can combine fragments of different
likely tokens into an invalid output.

## Two separate proofs

### Projected-code reconstruction

Condition the byte decoders directly on projected K32 embeddings and measure
exact token reconstruction on held-out complete token forms. Repeat after
adding controlled embedding noise. This isolates whether a compact decoder can
recover token structure from a Kronecker-derived representation.

### Multilingual next-token modeling

Train a two-layer decoder-only Transformer on balanced English, Hindi, Telugu,
and Kannada data. Compare token negative log-likelihood, exact decoded next
tokens, valid UTF-8 rate, parameters, output-layer memory, throughput, and
latency.

The byte loss is a proper string likelihood: sum byte and EOS negative
log-likelihood within each token, then average across target tokens. This is
directly comparable to the vocabulary head's token negative log-likelihood,
while bits per UTF-8 byte provides a length-normalized view.

## Long-token policy

All vocabulary tokens are retained. Tokens above 32 bytes use the original K32
input behavior identically in every compared model. Results are also reported
on the \(\le32\)-byte subset so input truncation cannot be mistaken for an
output-decoder failure. K32-O is not mixed into the active experiment.

## Core success criteria

The selected proposal succeeds if it demonstrates:

1. at least an eight-times output-parameter reduction;
2. at least a four-times reduction in peak output-logit tensor memory;
3. at least 99% exact clean reconstruction on supported held-out K32 forms;
4. at least 99% valid UTF-8 on natural-language test outputs;
5. validation token NLL within 10% of the vocabulary-head baseline;
6. greedy exact next-token accuracy within three absolute percentage points;
7. consistent three-seed results.

Greedy output latency within five times the vocabulary head is a separate
deployment-grade criterion. Failure there does not invalidate the compression
proof, but prevents a deployment-superiority claim.

## Claims we will not make

- The decoder makes output generation free.
- The hidden state is an exact inverse of a deterministic K32 code.
- Producing an unseen string means the model has learned facts about it.
- A 10,000-token CPU experiment proves production-scale superiority.
- Problem 3 has been solved as part of the output experiment.

# Implementation Outcome for Problem 5

The planned experiment was implemented and run under full profile
`d8dfc772972ced04`. Each architecture used the same Session 2 tokenizer and
corpora, K32 encoder, two-layer Transformer, data sampler, one-million-token
budget, and seed-specific shared backbone initialization. Two learning-rate
pilots selected `1e-3` for all heads, followed by seeds 7, 17, and 29.

## What the evidence proves

| Measure, mean over three seeds | Vocabulary head | Parallel byte | K-AR |
|---|---:|---:|---:|
| Output-head parameters | 1,290,000 | 66,177 | 140,673 |
| Validation token NLL | 8.221 ± 0.217 | 19.255 ± 0.140 | 12.557 ± 0.121 |
| Test greedy exact | 2.073% | 0.052% | 0.375% |
| Test beam exact | 2.865% | 0.000% | 2.083% |
| Test valid UTF-8 | 100.0% | 36.7% | 78.2% |
| Peak evaluation logits | 78.13 MiB | 21.25 MiB | 21.25 MiB |
| Greedy latency, ms/token | 0.008 | 0.049 | 0.390 |

K-AR passes the parameter target with a 9.17× smaller head. It also strongly
outperforms the parallel decoder, which is evidence that output-byte
dependencies cannot be ignored. Its beam result approaches the standard head
more closely than its greedy result, showing that search errors are one part of
the gap.

K-AR fails the main quality targets. Validation NLL is 52.7% above the
vocabulary baseline, valid UTF-8 is below 99%, peak logits memory improves only
3.68× rather than 4×, and greedy decoding is roughly 47× slower. Low
three-seed NLL variation shows these findings are stable under the tested
initializations; it does not make the quality gap acceptable.

## Reconstruction finding

On 1,998 stratified held-out vocabulary forms, K-AR clean exact reconstruction
is 4.40% overall and 4.54% for forms of at most 32 bytes. The parallel decoder
reaches 2.50% overall. K-AR produces valid UTF-8 for 99.95% of clean
reconstructions, but exact identity recovery is far below the declared 99%
target. A cosine search over a stored 10,000-entry codebook reaches 98.95%; this
is an upper reference, not a head-free solution, and it also exposes collisions
caused by shared 32-byte prefixes.

## Decision

Problem 5 has been answered experimentally, but the current K-AR design is not
a production replacement for the vocabulary head. The defensible claim is:

> A byte-autoregressive reverse head can remove vocabulary-sized parameters and
> is substantially better than independent byte prediction, but under this
> controlled CPU experiment it does not preserve language-model likelihood,
> UTF-8 validity, memory target, or decoding speed well enough to replace the
> standard head.

The next focused iteration should add UTF-8- or vocabulary-trie-constrained
decoding and teacher distillation. It should retain the same baselines and
success contract so improvements cannot be attributed to a changed input
encoder or an easier dataset.

# Deferred Alternative Proposal: K32-O — Backward-Compatible Kronecker Overflow

## Research question

Can we represent tokens longer than 32 UTF-8 bytes without changing the
embedding of ordinary K32 tokens and without paying the larger K64 projection
cost for every token?

## Design principle

Keep the original 32-byte block as the architectural primitive. Apply additional
machinery only when a token contains overflow bytes.

This protects the main strengths of Kronecker:

- unchanged K32 codec;
- unchanged first-block geometry;
- unchanged behavior for the overwhelming majority of tokens;
- shared \(8192\rightarrow d_{\text{model}}\) projection;
- active-byte sparse gathering;
- a clean fallback path for long tokens.

## Encoder

Split the UTF-8 byte sequence into non-overlapping blocks of at most 32 bytes:

\[
B_j=b_{32j+1:32(j+1)},\qquad
j=0,\ldots,N-1.
\]

Block boundaries are byte boundaries. If a boundary would split a UTF-8
codepoint, move the boundary backward to the preceding valid codepoint boundary.
Raw malformed byte sequences remain supported by an explicitly tested byte
fallback that does not attempt Unicode decoding.

Encode every block with the same original K32 codec and projection:

\[
x_j=\kappa_{32}(B_j)W_{\text{proj}}.
\]

The first block is the compatibility anchor:

\[
x_0=\text{original K32 representation}.
\]

Add a block-position representation only to overflow blocks:

\[
\tilde{x}_j=x_j+r_j,\qquad j\ge1.
\]

The block-position representation should use fixed sinusoidal features followed
by a small learned projection, avoiding an arbitrary hard limit on the number
of blocks.

## Overflow aggregation

The minimum viable aggregator is a small gated recurrent unit operating in a
reduced overflow width \(h\), not at full model width:

\[
u_j=P_{\text{down}}\tilde{x}_j,\qquad
s=\operatorname{GRU}(u_1,\ldots,u_{N-1}),
\]

\[
o=P_{\text{up}}s.
\]

The final token embedding is:

\[
z=x_0+g(L,N,x_0,o)\odot o.
\]

The gate is constrained so that:

\[
N=1\Rightarrow g=0\Rightarrow z=x_0.
\]

This equality must be enforced by control flow, not merely encouraged by a
loss. Therefore every token of at most 32 bytes is bitwise identical to the
original K32 path, subject to the same numerical kernel.

For long tokens, the model receives the original prefix representation plus a
learned residual summarizing all overflow blocks.

## Why a residual overflow path

Replacing \(x_0\) with a pooled representation would alter every K32 token and
discard the validated geometry of the original method. A gated residual:

- makes backward compatibility exact for short tokens;
- lets the model ignore unhelpful overflow information;
- localizes added parameters and computation;
- supports ablation by forcing the gate to zero;
- permits gradual curriculum introduction of long tokens.

## Normalization

Each block retains the original \(1/\sqrt{|B_j|}\) normalization. The overflow
aggregator receives the following explicit features:

- total byte length;
- number of blocks;
- current block index;
- current block byte length.

The final residual should be RMS-normalized before gating so that long tokens do
not receive embedding norms that grow with block count.

## Complexity

For byte length \(L\), \(N=\lceil L/32\rceil\).

- K32 path: unchanged for \(L\le32\).
- Long-token codec work: \(O(Ld_{\text{model}})\) active-row gathering and
  summation.
- Overflow aggregation: \(O((N-1)h^2)\) for a GRU of width \(h\).
- Temporary overflow memory: \(O(Nh)\) during training and \(O(h)\) for
  streaming inference.

Suggested proof configuration:

- \(d_{\text{model}}=128\);
- overflow width \(h=32\) or \(64\);
- one GRU layer;
- shared K32 projection;
- no separate projection per block.

At production scale, the serial GRU may be undesirable. The assignment should
also compare a parallel weighted-mean overflow aggregator. If the simple
aggregator performs similarly, it should be preferred.

## Formal properties to prove

### Determinism

For fixed parameters, byte segmentation, block encoding, block positions,
aggregation, and gating are deterministic.

### K32 compatibility

For every byte sequence \(b\) with \(|b|\le32\),

\[
\operatorname{K32O}(b)=\operatorname{K32}(b).
\]

This follows directly from the explicit short-token branch.

### No truncation within tested bounds

For every tested input, all bytes must be assigned to exactly one block. Record
source byte spans for each block and assert that their ordered concatenation is
the original input.

This proves processing completeness, not collision-free final embeddings.

### Fixed output shape

For all token lengths,

\[
\operatorname{K32O}(b)\in\mathbb{R}^{d_{\text{model}}}.
\]

### Complexity

Show that work grows with the number of actual bytes and overflow blocks, while
ordinary K32 tokens take the original path.

## Claims we will not make

- The final fixed-width float vector is injective for arbitrary strings.
- K32-O is mathematically reversible after its learned projection.
- Long tokens are always better represented merely because all bytes are read.
- Overflow recurrence is a new general sequence-model architecture.
- The aggregate truncation problem is important until measured on our data.
- Language-model quality improves until controlled experiments demonstrate it.

## Phase 0: measure the actual problem

Before training:

1. Load the Session 2 multilingual tokenizer artifacts and corpora.
2. Inspect every vocabulary token's UTF-8 byte length.
3. Report truncation rate by:
   - token type;
   - token frequency;
   - language/script;
   - byte-length bucket;
   - code, URL, identifier, and natural-language categories where detectable.
4. Measure token-mass truncation, not just vocabulary-row truncation.
5. Save representative affected examples.

This phase can invalidate the project. If truncation is negligible in both
vocabulary rows and observed token mass, the proposal should be presented as a
robustness extension rather than a likely quality improvement.

## Phase 1: invariant and adversarial tests

Test:

- byte lengths 0, 1, 31, 32, 33, 63, 64, 65, 256, and 4096;
- same 32-byte prefix with different suffixes;
- ASCII, Hindi, Telugu, Kannada, emoji, combining marks, and mixed scripts;
- repeated bytes;
- canonically equivalent but byte-distinct Unicode strings;
- malformed UTF-8 byte sequences;
- encoding alone versus inside differently padded batches.

Assertions:

- K32 truncates crafted same-prefix pairs to the same codec;
- K32-O consumes every byte;
- K32-O changes when an overflow byte changes;
- short-token output equals K32 exactly;
- block order changes the long-token output;
- no NaNs or infinities;
- gradients reach overflow bytes and overflow parameters;
- output is independent of batch padding.

## Phase 2: reconstruction probe

Train a byte decoder conditioned only on a token embedding.

### Data

- Session 2 English, Hindi, Kannada, and Telugu tokenizer vocabulary and text;
- long technical terms and identifiers from local session corpora;
- synthetic same-prefix adversarial pairs;
- held-out complete strings;
- length-disjoint split: train primarily on \(\le32\) bytes and evaluate
  separately on 33–64 and 65–128 bytes.

### Decoder

- one-layer autoregressive GRU;
- hidden width 128;
- 257 output classes: 256 bytes plus EOS;
- teacher-forced training;
- identical decoder capacity and training budget for every encoder.

### Baselines

1. Original K32.
2. K64, with its wider projection.
3. Prefix K32 plus byte-mean overflow.
4. Prefix K32 plus parallel weighted-mean overflow.
5. K32-O with GRU overflow.
6. A small byte-GRU token encoder without Kronecker structure.

### Metrics

- exact byte reconstruction;
- byte error rate;
- exact grapheme reconstruction;
- chrF;
- EOS and length accuracy;
- performance by language and byte-length bucket;
- same-prefix suffix discrimination;
- encoder parameters, latency, and peak memory.

Reconstruction is empirical evidence of retained information on a declared
distribution. It is not proof of injectivity.

## Phase 3: tiny multilingual language model

Keep the tokenizer, Transformer body, output head, optimizer, data order, and
training token budget identical across encoders.

Suggested model:

- two decoder-only Transformer layers;
- model width 128;
- four attention heads;
- FFN width 512;
- context length 128;
- approximately one million training tokens for the first complete run;
- balanced English, Hindi, Kannada, and Telugu sampling;
- three seeds for short runs and at least one full run per surviving design.

Use a standard untied vocabulary output head. Problem 5 must not be mixed into
this experiment.

Report:

- validation negative log-likelihood and perplexity;
- bits per UTF-8 byte;
- per-language loss;
- loss by token byte-length bucket;
- long-token next-token accuracy;
- typo and suffix-variation robustness;
- trainable parameter count;
- CPU tokens per second;
- p50 and p95 encoder latency;
- peak resident memory.

## Essential ablations

- gate forced to zero;
- GRU versus parallel weighted mean;
- overflow width 16, 32, and 64;
- shared versus independent block projection;
- fixed versus learned block positions;
- with and without total-length features;
- UTF-8-safe block boundaries versus raw fixed 32-byte boundaries;
- training with natural long-token frequency versus an oversampled long-token
  curriculum;
- K32, K64, and parameter-matched controls.

## Success criteria

The proposal succeeds as an assignment if:

1. short-token embeddings are exactly compatible with K32;
2. no input bytes are silently dropped in the tested range;
3. same-prefix long-token discrimination is near perfect;
4. long-token reconstruction improves substantially over K32;
5. overall LM loss remains within 3% of K32 under matched training;
6. long-token or affected-script loss improves;
7. K32 tokens incur no meaningful latency regression;
8. the overflow path uses materially fewer parameters than moving globally to
   K64.

Any claimed LM-quality improvement must include seed variance.

## Kill and downgrade criteria

Downgrade or reject the approach if:

- the measured affected token mass is negligible;
- a simple byte-mean overflow matches the learned aggregator;
- the model consistently learns to close the overflow gate;
- K64 performs better at acceptable parameter cost;
- long-token gains vanish under parameter or compute matching;
- GRU latency materially reduces end-to-end throughput;
- reconstruction improves but language-model loss does not;
- overflow training destabilizes curriculum transitions;
- results depend on synthetic long strings but not real corpus tokens.

Negative findings remain useful. In particular, demonstrating that the 32-byte
limit is statistically harmless would be a valid result and would argue
against adding unnecessary architectural complexity.

## Deliverables

```text
session7/
├── README.md
├── PROBLEM_ANALYSIS_AND_PROPOSAL.md
├── requirements.txt
├── src/
│   ├── data.py
│   ├── encoders.py
│   ├── reconstruction.py
│   ├── transformer.py
│   └── evaluation.py
├── experiments/
│   ├── analyze_lengths.py
│   ├── run_invariants.py
│   ├── run_reconstruction.py
│   └── run_language_model.py
├── tests/
│   ├── test_k32_compatibility.py
│   ├── test_overflow_coverage.py
│   └── test_determinism.py
├── artifacts/
│   ├── corpus_length_analysis.json
│   ├── reconstruction_results.json
│   └── language_model_results.json
└── report/
    └── index.html
```

The report should visualize:

- the 256-by-32 K32 coordinate layout;
- UTF-8 bytes and grapheme clusters for multilingual examples;
- exact truncation points;
- K32-O block construction;
- the compatibility path for short tokens;
- suffix discrimination for common-prefix adversarial examples;
- reconstruction quality versus byte length;
- accuracy, parameters, latency, and memory for each baseline.

## Deferred decision

K32-O remains the recommended design if Problem 3 is pursued later: preserve 32
as the local factor and add a strictly conditional overflow path. It is not the
active assignment because Problem 5 has greater potential impact and must be
tested independently.

# Final Decision

The active assignment targets Problem 5 with K-AR. The required evidence is a
controlled comparison against a standard vocabulary head and a parallel byte
decoder, using the same K32 input encoder and Transformer body. Projected-code
reconstruction establishes recoverability; multilingual language modeling
establishes whether the structured decoder remains useful under genuine
probabilistic next-token uncertainty.
