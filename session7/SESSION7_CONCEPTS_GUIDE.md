# Session 7 — Embeddings and Kronecker Embedding V2

> A plain-language guide to the problem, the proposed idea, what went wrong, and what the assignment asks us to solve next.

**Source:** `Session7_Transcript.md` and `assignment.md`  
**Session date:** 8 August 2026

---

## Read this first: the session in one page

A tokenizer converts text into token IDs. For example, it might convert `apple` into token ID `47`. But `47` is only an address—it does not contain the meaning of *apple*. Before a transformer can process it, the model uses an **embedding layer** to turn that ID into a vector of numbers.

The usual embedding layer is a large table:

```text
number of rows    = vocabulary size
numbers per row   = embedding dimension
total parameters  = vocabulary size × embedding dimension
```

For a vocabulary of 131,072 tokens and an embedding dimension of 8,192, the table contains:

```text
131,072 × 8,192 = 1,073,741,824 parameters
```

That is more than one billion parameters just to get tokens into the transformer. A separate output head can require another matrix of the same size.

**Kronecker embedding V1 asks:** can we construct the vector from the token's own characters or bytes instead of storing one learned row for every vocabulary item?

Its proposed answer is:

```text
token text
   ↓
UTF-8 bytes + byte positions
   ↓
fixed deterministic code
   ↓
small shared learned projection
   ↓
vector consumed by the transformer
```

This is attractive because the learned input embedding no longer has to grow with vocabulary size. It also exposes spelling and byte structure to the model.

However, V1 has serious limitations:

- It reserves a fixed window of 32 bytes for every token.
- Short tokens waste most of the window.
- Tokens longer than 32 bytes must be split, rejected, or cropped.
- Many Indic characters require three UTF-8 bytes, so the effective character limit can fall to roughly ten characters.
- The shared projection can become unstable when the training-data mixture changes suddenly.
- The reported small-model experiment was encouraging, but not conclusive at large scale.
- The construction works deterministically from token to vector, but reliable reverse decoding from an approximate model output back to a token remains unsolved.

**Kronecker V2 is the search for a solution to one of these open problems.** The assignment gives five independent directions: mathematical structure, multimodality, dynamic length, Fourier encoding, or reverse decoding.

---

## 1. What is an embedding?

An embedding is a list of numbers used to represent an input in a form a neural network can process.

Suppose the tokenizer produces this:

```text
"the sun rises" → [97, 103, 46]
```

The integers are token IDs. Each ID selects a row from the embedding table:

```python
# Conceptual shapes
token_ids = [batch, sequence]          # integers
E         = [vocabulary, embedding_d]  # learned embedding table

x = E[token_ids]                       # [batch, sequence, embedding_d]
```

If token `47` means `apple`, then `E[47]` might be an 8,192-dimensional vector.

### Token ID versus embedding

These are easy to confuse:

- **Token ID:** an address in a vocabulary, such as `47`.
- **Embedding:** the dense vector stored at or constructed for that address.

The number `47` does not mean *apple* by itself. The learned vector is what the model uses.

### What does each embedding dimension mean?

The session used **bandwidth** as the intuition. More dimensions give the model more capacity to represent distinctions and relationships.

However, dimension 14 does not necessarily mean “is a company,” and dimension 25 does not necessarily mean “is red.” Neural networks usually distribute concepts across many dimensions. This is why modern deep learning largely replaced manual feature engineering.

For example, the base representation of `bank` must be usable in several contexts:

- a financial institution;
- the bank of a river;
- banking a road or aircraft.

The base embedding starts the representation. The transformer uses surrounding tokens to create the context-specific meaning.

---

## 2. How an ordinary embedding table actually operates

Embedding lookup is sometimes explained as multiplying a one-hot vector by the whole embedding matrix. That is mathematically valid but operationally misleading.

In practice, the system performs a **gather**: it reads the requested rows.

```python
import torch

embedding = torch.nn.Embedding(
    num_embeddings=131_072,
    embedding_dim=8_192,
)

token_ids = torch.tensor([[47, 11, 902]])
x = embedding(token_ids)

print(x.shape)  # [1, 3, 8192]
```

Reading three rows is cheap. The expensive part is storing and training all 131,072 rows.

### What happens during backpropagation?

Assume `the` appears 67 times in a batch.

1. The forward pass gathers its row 67 times.
2. Backpropagation produces 67 gradient contributions for that row.
3. Those contributions are accumulated.
4. The optimizer applies the combined update for that training step.

Rows belonging to tokens absent from the batch receive no embedding update during that step.

---

## 3. Zipf's law and uneven learning

Natural language follows a long-tail frequency pattern known as **Zipf's law**:

- a small number of tokens occur extremely often;
- many tokens occur rarely.

This matters because a frequently occurring embedding row receives many more gradient contributions than a rare one.

```text
"the"             → seen constantly → many updates
specialized term  → seen rarely     → few updates
```

This is especially important for lower-resource languages. There may already be less Indic training data, and the less-common words inside that data receive even fewer updates.

Optimizers such as AdamW can adjust the size of parameter updates using their history. Data-mixture policies can also increase underrepresented material. But neither eliminates the underlying long tail.

### Important distinction

A token ID can be assigned according to frequency—for example, common tokens may receive smaller IDs. But the ID only gives an ordering. Zipf's law describes how large the frequency differences actually are.

---

## 4. The cost of a standard embedding table

For vocabulary size `V` and embedding dimension `d`:

```text
input embedding parameters = V × d
```

Using the intended Session 7 numbers:

```python
V = 131_072
d = 8_192

parameters = V * d
print(parameters)  # 1,073,741,824
```

If the weights are stored in BF16, the weights alone occupy about 2 GiB. Training requires additional memory for gradients, optimizer moments, and sometimes higher-precision master weights.

The session used roughly **16 bytes per trainable parameter** as an AdamW planning estimate. The exact number depends on the implementation, precision, sharding, and optimizer.

> **Clarification:** parameter memory is not copied once for every item in the batch. Increasing batch size mainly increases activations and temporary buffers. The model weights and optimizer state remain one copy per model replica or shard.

### A note about “8096” in the transcript

The transcript repeatedly says `8096`, but the described construction uses:

```text
32 positions × 256 byte values = 8192
```

It later also mentions an `8192 → 4096` projection. This guide therefore uses **8192** as the intended value and treats `8096` as a transcription error.

---

## 5. Tokenizer size, fertility, and embedding cost

The tokenizer and embedding layer must be designed together.

**Fertility** is approximately the number of tokens required to represent some text. Lower fertility means the transformer processes fewer tokens.

| Choice | Benefit | Cost |
|---|---|---|
| Smaller vocabulary | Smaller input and output matrices | More tokens per sentence and more attention compute |
| Larger vocabulary | Longer/common words can be single tokens; lower fertility | Larger embedding table and output head |

For example:

```text
smaller vocabulary: "manuscript" → ["manu", "script"]
larger vocabulary:  "manuscript" → ["manuscript"]
```

A larger vocabulary reduces sequence length, but every added vocabulary item normally adds another embedding row and another output score.

The best choice depends on:

- the actual language and domain mixture;
- measured tokenizer fertility;
- model width;
- GPU memory;
- training and inference compute;
- hardware-friendly matrix sizes.

---

## 6. The output head and weight tying

The transformer produces a hidden vector of dimension `d`. The **output head** converts it into `V` scores—one for every possible next token.

```text
transformer output: [d]
        ↓
output matrix: [d, V]
        ↓
logits: [V]
        ↓
softmax / sampling
        ↓
next token
```

The output matrix has approximately the same parameter count as the input embedding table.

### Weight tying

Weight tying reuses the input embedding matrix, transposed, as the output head.

Benefits:

- saves `V × d` parameters;
- can act as a useful regularizer;
- often makes sense for smaller language models.

Trade-off:

- input representations and output classification cannot specialize independently.

The session's rule of thumb was to tie smaller models and prefer an untied output head for larger models. This is an empirical design choice, not a mathematical requirement.

---

## 7. Low-rank factorization

A large transformation can sometimes be approximated by two smaller matrices with a bottleneck rank `r`:

```python
# Full transformation
y = x @ W                 # W: [8192, 8192]

# Low-rank approximation
y = (x @ A) @ B           # A: [8192, r], B: [r, 8192]
```

If `r` is much smaller than 8,192, this reduces parameters and computation.

This is generally an approximation, not exact equality, unless the full matrix truly has rank `r`. The useful rank must be measured. It may differ by layer and change as training progresses.

The session connected this intuition to **LoRA: Low-Rank Adaptation**, where small low-rank matrices are trained instead of changing every parameter in a large model.

---

## 8. What is Kronecker embedding?

### The motivating question

The transformer only needs a `d`-dimensional vector. It does not care whether that vector came from a vocabulary lookup table or another deterministic construction.

So the proposal is:

> Can we generate the token vector from the token's own structure and avoid storing a learned row for every vocabulary item?

### Why is it called “Kronecker”?

The **Kronecker product** combines every element of one vector with every element of another.

For two vectors:

```text
a = [a₁, a₂]
b = [b₁, b₂, b₃]

a ⊗ b = [a₁b₁, a₁b₂, a₁b₃, a₂b₁, a₂b₂, a₂b₃]
```

In the Session 7 construction, we can think of:

- one one-hot vector selecting a byte position from 32 possibilities;
- one one-hot vector selecting a byte value from 256 possibilities.

Their Kronecker product identifies one unique position–byte pair:

```text
32 positions × 256 byte values = 8192 features
```

### V1 construction

For every token:

1. Encode the token as UTF-8 bytes.
2. Keep at most 32 bytes.
3. Combine each byte with its position.
4. Sum or average the resulting fixed features.
5. Pass the fixed vector through one shared learned projection.

```python
import torch

def kronecker_code(text: str, max_bytes: int = 32):
    raw = text.encode("utf-8")

    if len(raw) > max_bytes:
        raise ValueError("token exceeds the 32-byte window")

    # One feature for every possible (position, byte) pair.
    x = torch.zeros(max_bytes * 256)  # 8192 dimensions

    for position, byte_value in enumerate(raw):
        feature_index = position * 256 + byte_value
        x[feature_index] = 1.0

    # Prevent longer strings from having a much larger magnitude.
    return x / max(1, len(raw))


d_model = 4096

# This projection is shared by every token. There is no learned row per token.
projection = torch.nn.Linear(8192, d_model, bias=False)

fixed_code = kronecker_code("apple")
embedding = projection(fixed_code)
```

This code is an explanatory version of the construction described in the session. An implementation can use an equivalent structured or fixed random projection. The important separation is:

```text
deterministic token code + shared learned adapter
```

### Worked example: `apple`

| Position | Character | UTF-8 byte | Active feature |
|---:|:---:|---:|---:|
| 0 | `a` | 97 | `0 × 256 + 97` |
| 1 | `p` | 112 | `1 × 256 + 112` |
| 2 | `p` | 112 | `2 × 256 + 112` |
| 3 | `l` | 108 | `3 × 256 + 108` |
| 4 | `e` | 101 | `4 × 256 + 101` |

The two `p` characters remain distinguishable because their positions differ.

Every occurrence of the same byte sequence produces the same base code. Context is added later by transformer layers. Thus `apple` can still mean a fruit, a company, or a metaphor depending on the sentence.

---

## 9. Why use Kronecker embedding?

### 9.1 Reduce trainable input parameters

A standard input table grows as:

```text
V × d
```

A shared projection can be independent of `V`. This is potentially a large saving when the vocabulary is large.

### 9.2 Expose spelling and byte structure

An ordinary token ID does not tell the transformer how the token is spelled. A byte-and-position construction gives the input path access to that structure.

### 9.3 Share learning across tokens

In a row lookup table, a rare token mostly learns through its own rare row. In a shared character/byte construction, many tokens use the same underlying machinery.

For example, the strings below share several byte features:

```text
apple
apply
apples
```

This does not guarantee similar meaning, but it gives the model reusable internal structure.

### 9.4 Construct a code for an unseen string

Any byte sequence that fits the window can receive a deterministic code even if it never had a learned embedding row.

This is different from claiming the tokenizer automatically treats any arbitrary phrase as one token. The tokenizer—or an additional span-packing policy—must still decide what unit is passed to the embedding function.

### 9.5 Separate base identity from contextual meaning

The deterministic code describes the token's surface form. The transformer is still responsible for contextualizing it.

This separation is sensible because even an ordinary learned embedding is not the final meaning of a token. Its meaning changes through the transformer layers.

---

## 10. What problems did Kronecker V1 run into?

### 10.1 Fixed 32-byte capacity

Every token is designed against the same 32-byte window:

```text
"a"     → uses 1 byte, leaving 31 unused
"apple" → uses 5 bytes, leaving 27 unused
```

A token above 32 UTF-8 bytes must be split, rejected, or cropped. Cropping is particularly dangerous because two long strings with the same first 32 bytes become identical to the encoder.

### 10.2 It is a byte limit, not a character limit

ASCII characters normally use one UTF-8 byte. Many Indic characters use three bytes, and combining marks add more.

```python
samples = [
    "internationalization",
    "namaste",
    "नमस्ते",
]

for text in samples:
    print(
        text,
        "characters =", len(text),
        "UTF-8 bytes =", len(text.encode("utf-8")),
    )
```

Therefore, the same 32-byte budget may hold around 32 ASCII characters but only around ten Indic characters—sometimes fewer.

**Impact:** a design intended to support Indic languages can accidentally impose a much stricter usable word-length limit on them.

### 10.3 Short strings waste reserved capacity

The model has an 8,192-dimensional position-byte space even when only one or two byte positions are active. The representation is sparse, but the shared dense projection can still perform an 8,192-wide operation.

V2's dynamic-length problem asks whether the computation and representation can scale with actual length without losing order.

### 10.4 Sudden data-mixture changes can shock the projection

The session reported loss spikes when the curriculum changed abruptly—for example, from simpler/common English to specialized vocabulary.

The shared projection sees every token. A sudden input-distribution change can therefore create a sharp gradient shift at this bottleneck.

The proposed operational mitigation was:

- change mixture ratios gradually;
- use warm-up during transitions;
- control the learning rate;
- monitor the projection separately from the transformer stack.

### 10.5 The available experiment was not conclusive

The session describes testing at roughly 121–131 million parameters and seeing encouraging predictions. But there was not enough GPU time for a convincing large-model comparison.

Claims still needing controlled proof include:

- better handling of rare tokens;
- useful behavior for misspellings or unseen forms;
- equal or better language-model quality;
- Indic-language benefits;
- real memory and throughput savings;
- stable large-scale training.

### 10.6 Reverse decoding is unresolved

Forward construction is exact:

```text
token → deterministic vector
```

Generation requires the reverse:

```text
model output → token
```

The problem is that a neural network predicts approximate continuous numbers.

```text
target code:    [0.30, 0.20, 0.10, 0.30, ...]
model predicts: [0.31, 0.18, 0.09, 0.29, ...]
```

Exact equality will not work.

Nearest-neighbor or cosine search is also not a complete solution:

- early in training, predictions may be far from every valid code;
- codes must be separated enough to tolerate noise;
- searching a million candidates may recreate a large-vocabulary cost;
- similar vectors must still decode uniquely.

The session mentions KL divergence and VAE-style distributions as a possible way to predict regions rather than exact points. This could provide noise tolerance, but it does not by itself guarantee unique or efficient decoding.

**Why this matters:** reliable reverse decoding could remove the large `d × V` output head. Until that is solved, Kronecker V1 mainly reduces the input-side table, not the full language-model vocabulary interface.

---

## 11. Why positional information is required

Transformer tokens are processed in parallel. Without position information, the core computation has no inherent reason to distinguish:

```text
A before B
```

from:

```text
B before A
```

The session introduced four position families.

| Method | How position enters | Main point |
|---|---|---|
| Learned absolute | Learned vector for each sequence position, added near input | Positions beyond training are unlearned; table grows with maximum context |
| Sinusoidal | Fixed sine/cosine functions added near input | No learned table, but very long-range resolution and extrapolation can be weak |
| RoPE | Rotates query and key features inside attention | Encodes relative position effectively; common in modern LLMs |
| ALiBi | Adds a distance-dependent bias to attention scores | Simple, inexpensive relative-position bias |

### Two different kinds of position

Kronecker also uses position inside a token:

- **Byte position:** the location of `p` inside `apple`.
- **Sequence position:** the location of the `apple` token inside a sentence.

These solve different problems and may be implemented in different parts of the model.

---

## 12. Other training inputs mentioned in the session

The session briefly described the information prepared with a batch.

### Token IDs

The tokenizer's integer outputs.

```text
[97, 103, 46, ...]
```

### Position IDs or position policy

Information that lets the model distinguish ordering.

### Loss mask

A loss mask says which token positions contribute to the training loss.

For ordinary next-token pretraining, most valid token positions contribute. For question-answer or instruction tuning, the prompt tokens may be masked so the loss is calculated only on the desired answer.

```python
# Simplified illustration
tokens    = [question tokens..., answer tokens...]
loss_mask = [0, 0, 0, 0,          1, 1, 1, 1]
```

### Mixture and ledger metadata

Information such as language/domain lane, curriculum stage, run ID, step, and shard ID may not enter the model directly, but it is needed for training control, auditing, and reproducibility.

---

## 13. What are we trying to solve now? The five V2 directions

The assignment says to choose **one** problem. The five problems are separate research directions.

### 13.1 Store mathematical structure in embeddings

**Goal:** make some part of the representation preserve mathematical operations.

Examples proposed in the assignment:

```text
embedding(9) + embedding(9) → representation of 18
operation(embedding(9), ×, embedding(9)) → representation of 81
```

The precise mathematical idea is an **operation-preserving representation**.

Addition can be represented linearly in a numeric subspace:

```text
value_vector(a) + value_vector(b) = value_vector(a + b)
```

Multiplication is harder to make linear in the same coordinates. For positive values, logarithms turn multiplication into addition:

```text
log(a × b) = log(a) + log(b)
```

One possible research sketch is:

```python
embedding(n) = concat(
    language_features(n),
    numeric_value_features(n),
    log_value_features(n),
)

addition_loss = distance(
    decode_value(embedding(a) + embedding(b)),
    a + b,
)

multiplication_loss = distance(
    decode_log(embedding(a)) + decode_log(embedding(b)),
    log(a * b),
)
```

**What would prove it?** Test numbers and combinations that never appeared in training. Compare arithmetic accuracy and ordinary language-model quality with a same-size baseline.

### 13.2 Extend the construction to text, images, and audio

**Goal:** use a common structured-embedding idea for all three modalities.

One possible mapping is:

| Modality | Local content unit | Position information |
|---|---|---|
| Text | UTF-8 byte or character code | Position inside the token/span |
| Image | Patch, discrete visual code, or pixel feature | 2D row and column |
| Audio | Short-time spectral or codec code | Time index and possibly frequency band |

A modality identifier is important so code `42` in text does not collide semantically with code `42` in an image or audio codec.

```text
content code + local position + modality ID → shared projection
```

**What would prove it?** Report performance for all three modalities and at least one cross-modal task, such as image-text retrieval. Ablate the modality and position codes to show what each contributes.

### 13.3 Make the 32-byte window dynamic

**Goal:** allow cost to depend on actual length and remove hard cropping.

Possible approaches include:

- sparse gathers over only the active position-byte features;
- chunk a long token and combine chunk summaries hierarchically;
- use a variable-length byte encoder followed by pooling;
- use recurrent or rolling structured hashes with collision controls;
- allocate multiple blocks only when the token requires them.

A good solution must preserve order, avoid harmful collisions, support long strings, and keep computation bounded.

**What would prove it?** Compare truncation rate, validation loss, speed, and memory across lengths. Include both ASCII and Indic strings rather than testing English alone.

### 13.4 Build a real Fourier alternative

**Goal:** represent each byte or character as a wave and combine a token by adding the waves.

A conceptual complex-valued construction is:

```text
code(token) = Σᵢ amplitude(byteᵢ) × exp(j × frequency(byteᵢ) × positionᵢ)
```

Fourier-style codes are attractive because addition is fast and position can be expressed as phase. But a naïve sum can lose ordering or produce collisions.

Questions the solution must answer:

1. Can different strings produce the same or almost the same spectrum?
2. Are anagrams distinguishable?
3. Can the original sequence be recovered under prediction noise?
4. Does it generalize to lengths not seen during training?
5. Is it actually faster than the Kronecker construction?

**What would prove it?** Perform collision analysis, reconstruction tests, noise tests, and a controlled language-model comparison. A visually appealing frequency plot alone is not proof.

### 13.5 Make Kronecker reversible

**Goal:** reliably decode an approximate neural output into the original token and remove the `V`-way output head.

Possible directions include:

- **error-correcting structured codes:** valid tokens occupy well-separated regions with known decoding rules;
- **autoregressive byte decoder:** predict length and bytes from the hidden state;
- **vector quantization:** snap the continuous output to a discrete valid code;
- **factorized prediction:** separately predict length, byte values, and positions;
- **probabilistic decoding:** predict distributions rather than exact coordinates.

The solution must work throughout training. It is not enough to show that nearest-neighbor decoding works after a mature model already predicts vectors close to valid codes.

**What would prove it?** Measure:

- exact token recovery;
- next-token accuracy or perplexity;
- robustness to controlled output noise;
- decoding speed;
- memory use;
- behavior from early training onward;
- scaling as the candidate vocabulary approaches one million tokens.

> Solving reverse decoding would not make a one-million-token system completely free. Tokenizer construction, data coverage, training stability, and decoding work still matter. It could, however, remove the dominant dense output matrix if decoding is genuinely sublinear in vocabulary size.

---

## 14. What counts as proof for the assignment?

A small transformer is enough if the experiment isolates the chosen claim and uses a fair comparison.

### Minimal experiment

1. **State one measurable hypothesis.**

   Example: “The dynamic encoder eliminates truncation and achieves equal or lower validation loss than fixed-32 Kronecker at the same trainable-parameter budget.”

2. **Implement three systems.**

   - ordinary learned embedding baseline;
   - Kronecker V1 baseline;
   - proposed V2 method.

3. **Match the important budgets.**

   Use the same transformer depth, model width, training tokens, optimizer, training steps, and—where possible—comparable trainable parameters or FLOPs.

4. **Design data that exposes the target problem.**

   A dynamic-length experiment needs long multilingual strings. A reverse-decoding experiment needs many candidate tokens and controlled output noise. A math experiment needs unseen operand combinations.

5. **Keep a real held-out split.**

   Test unseen combinations, not only new examples generated from the exact same templates.

6. **Measure quality and efficiency.**

   Report model quality, parameters, peak memory, throughput, and failure cases.

7. **Use multiple random seeds if possible.**

   Small neural experiments can appear successful by chance.

### Metrics by chosen problem

| Problem | Primary evidence | Important stress test |
|---|---|---|
| Mathematical structure | Held-out operation accuracy and structural consistency | Numbers and compositions absent from training |
| Multimodal | Quality per modality and cross-modal retrieval | Remove modality or position codes |
| Dynamic length | Zero truncation, quality by length, speed and memory | Long Indic and ASCII strings; collision tests |
| Fourier | Reconstruction/collision rate and language-model quality | Noise, long sequences, permutations and anagrams |
| Reverse decoding | Exact recovery and next-token quality | Early training, output noise, very large candidate set |

### Suggested README structure

1. Problem chosen and why it matters.
2. Proposed mechanism, including tensor shapes.
3. One small worked example.
4. Assumptions and expected failure modes.
5. Baselines and fairness controls.
6. Dataset and train/validation split.
7. Results table and plots.
8. Ablations and negative results.
9. Exact reproduction commands.
10. A conclusion limited to what the evidence proves.

---

## 15. Common confusions resolved

| Confusion | Resolution |
|---|---|
| Token ID and embedding are the same | The ID is an address; the embedding is the dense vector read or constructed for it. |
| Embedding dimension and model width are always the same | They can be equal, but do not have to be. A projection connects them when they differ. |
| Token position and byte position are the same | Token position orders tokens in the sentence; byte position orders bytes inside one token. |
| Kronecker replaces the tokenizer | No. The tokenizer still decides the spans presented as tokens. Kronecker changes how those tokens become vectors. |
| Deterministic means non-contextual forever | Only the base code is deterministic. Transformer layers still contextualize it. |
| Standard learned embeddings are random every time | No. After training, the same token ID retrieves the same learned row at inference. Kronecker's difference is that the base vector is algorithmically generated from token content. |
| Removing the input table also removes the output head | No. V1 solves only the input construction unless reverse decoding is also solved. |
| Cosine similarity makes reversal easy | Only if outputs already land near uniquely separated valid codes and search is affordable. This is weakest early in training. |
| KL divergence guarantees reversibility | It can help predict distributions or tolerant regions, but uniqueness and efficient decoding still require a code design. |
| The V1 limit is 32 characters | It is effectively 32 UTF-8 bytes, which is much stricter for multi-byte scripts. |
| A larger vocabulary is always better | It lowers fertility but increases embedding and output cost. The correct point depends on data and hardware. |

---

## 16. PyTorch terms the session expects you to recognize

The session also recommended a quick PyTorch review before later model-internals classes.

### Tensor

A multidimensional array.

```python
import torch

x = torch.randn(2, 16, 4096)
# batch = 2, sequence = 16, model width = 4096
```

### Module

A reusable neural-network component containing operations and possibly parameters.

```python
class TinyModel(torch.nn.Module):
    def __init__(self, vocab_size, d_model):
        super().__init__()
        self.embedding = torch.nn.Embedding(vocab_size, d_model)
        self.head = torch.nn.Linear(d_model, vocab_size)

    def forward(self, token_ids):
        x = self.embedding(token_ids)
        return self.head(x)
```

### Forward, loss, backward, optimizer step

```python
logits = model(token_ids)          # forward pass
loss = loss_function(logits, targets)

optimizer.zero_grad()
loss.backward()                    # calculate gradients
optimizer.step()                   # update parameters
```

### Shape discipline

Most errors in transformer code are easier to diagnose when every tensor's shape is written down.

```text
token IDs     [B, T]
embeddings    [B, T, d]
logits        [B, T, V]
targets       [B, T]
loss mask     [B, T]
```

---

## 17. Final mental model

Ordinary embedding says:

> “Look up the learned row for this token.”

Kronecker V1 says:

> “Construct a stable code from the token's bytes and their positions, then pass it through one shared learned adapter.”

The intended impact is to reduce vocabulary-dependent input parameters, expose spelling structure, and give rare or unseen strings a constructible representation.

The cost is a fixed 32-byte boundary, unequal capacity across scripts, possible projection instability, incomplete experimental proof, and no reliable reverse decoder.

Kronecker V2 asks how to keep the useful structured construction while solving **one** of those limitations convincingly.

---

## Glossary

**Embedding:** a dense numeric vector representing an input unit.

**Fertility:** how many tokens are required to represent some text.

**Gather:** selecting rows from an embedding table using token IDs.

**Kronecker product:** a structured combination of two vectors; here it can identify a byte value at a particular byte position.

**Loss mask:** a binary or weighted mask that determines which token positions contribute to training loss.

**Model width:** the size of the hidden vector processed by transformer blocks.

**Output head:** the mapping from the transformer's hidden state to one score per vocabulary token.

**Rank:** the number of independent directions represented by a matrix; low-rank factorization uses a narrower bottleneck.

**RoPE:** rotary position embedding, applied inside attention to query/key features.

**Weight tying:** reusing input embedding weights for the output head.

**Zipf distribution:** a frequency pattern with a few very common items and a long tail of rare items.

