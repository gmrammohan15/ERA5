# Session 6 Concepts Guide: Data Ledger, Shards, Packing, Replay

This guide explains the main ideas from Session 6 in assignment-ready terms. The lecture is about converting a human training-data plan into an executable system that can feed a model, track what happened, resume after crashes, and replay the same data order later.

The central object is the **data ledger**.

```text
raw documents
-> cleaned documents
-> frozen tokenizer
-> tokenized shards + manifests
-> packed training sequences
-> microbatches/global batches
-> fake training loop
-> checkpoint
-> crash/resume
-> replay from ledger
```

For the assignment, you do not need to train a real LLM. You need to demonstrate the full data path with small data and fake training.

---

## 1. Raw Document

A **document** is one piece of source data before it becomes model input. It can be a web article, code file, Indic text, instruction-answer pair, or agent trace.

Example:

```json
{
  "doc_id": "web_001",
  "type": "web",
  "language": "en",
  "text": "India is a large country with many languages.",
  "source": "toy_web_dataset",
  "license": "demo"
}
```

What you need to know:

- Keep a stable `doc_id`.
- Keep provenance: where the document came from.
- Keep data type: web, code, Indic, SFT, agent trace, etc.
- Do not lose metadata when converting to tokens.

---

## 2. Cleaning

**Cleaning** prepares raw data before tokenization. This may remove HTML, duplicate content, bad formatting, personal information, or evaluation contamination.

Simple example:

```python
def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = " ".join(text.split())
    return text.strip()

raw = " India   is \n\n a country. "
clean = clean_text(raw)
print(clean)  # "India is a country."
```

In real training, you must track the cleaning pipeline hash so that you know exactly which cleaning code produced a shard.

```python
import hashlib

cleaning_code = "clean_text_v1_strip_whitespace"
cleaning_hash = hashlib.sha256(cleaning_code.encode()).hexdigest()
```

Assignment point:

- Your manifest should mention the cleaning version/hash.

---

## 3. Tokenizer

A **tokenizer** converts text into token IDs.

Example:

```text
"India is great"
-> ["India", "is", "great"]
-> [11, 4, 29]
```

Tiny toy tokenizer:

```python
class ToyTokenizer:
    def __init__(self, vocab):
        self.vocab = vocab
        self.unk_id = vocab["<UNK>"]

    def encode(self, text: str) -> list[int]:
        return [self.vocab.get(word, self.unk_id) for word in text.split()]

vocab = {
    "<PAD>": 0,
    "<EOS>": 1,
    "<UNK>": 2,
    "India": 3,
    "is": 4,
    "great": 5,
}

tokenizer = ToyTokenizer(vocab)
print(tokenizer.encode("India is great"))  # [3, 4, 5]
```

What “frozen tokenizer” means:

- Once training shards are created, the tokenizer must not change.
- If the tokenizer changes, old token IDs may no longer mean the same thing.
- Store a tokenizer hash in every shard manifest.

```python
import json, hashlib

tokenizer_json = json.dumps(vocab, sort_keys=True)
tokenizer_hash = hashlib.sha256(tokenizer_json.encode()).hexdigest()
```

---

## 4. Token IDs

**Token IDs** are integers that represent tokens. Models do not directly train on raw text. They train on token IDs.

Example:

```python
tokens = [3, 4, 5, 1]
# 3 = India
# 4 = is
# 5 = great
# 1 = <EOS>
```

For training, each sample usually becomes a fixed-length list:

```python
sequence_length = 8
sample = [3, 4, 5, 1, 0, 0, 0, 0]
# real tokens + EOS + PAD tokens
```

---

## 5. EOS, BOS, PAD

### EOS

**EOS** means end of sequence/context/document. It tells the model that one context ended and a new one may begin.

```text
"India is great" + <EOS> + "Python is useful" + <EOS>
```

As token IDs:

```python
EOS = 1
doc1 = [3, 4, 5]
doc2 = [6, 4, 7]
packed = doc1 + [EOS] + doc2 + [EOS]
```

Why EOS matters:

- Without EOS, the model may learn unnatural transitions between unrelated documents.
- With EOS, backpropagation can teach the model that previous context should not be used after the boundary.

### BOS / SOS

**BOS** or **SOS** means beginning of sequence. The lecture mentions that some training strategies use it, but many modern pipelines mainly rely on EOS to save token space.

```python
BOS = 8
sample = [BOS] + doc1 + [EOS]
```

### PAD

**PAD** is a filler token used to make all samples the same length.

```python
PAD = 0
sequence_length = 8
tokens = [3, 4, 5, EOS]
tokens = tokens + [PAD] * (sequence_length - len(tokens))
print(tokens)  # [3, 4, 5, 1, 0, 0, 0, 0]
```

Important:

- Padding wastes compute.
- Loss should usually not be calculated on PAD tokens.

---

## 6. Sequence Length / Context Length

**Sequence length** is the number of tokens in one training sample.

Example:

```python
sequence_length = 8
sample = [3, 4, 5, 1, 6, 4, 7, 1]
```

In real training, this may be:

```text
4096, 8192, 32768, 128000, ...
```

If a model is trained with a max context of 4096, inference with 2048 tokens is fine because it is shorter. The harder question is whether it works well with more than 4096.

---

## 7. Tokenized Shard

A **tokenized shard** is an immutable chunk of already-tokenized training data.

Instead of storing only text:

```text
India is great.
Python is useful.
```

you store token IDs:

```json
[
  [3, 4, 5, 1],
  [6, 4, 7, 1]
]
```

Why shards exist:

- Tokenization is expensive; do it before training.
- Shards can be streamed into training.
- Shards can be hashed and tracked.
- Resume/replay becomes possible.

Example shard file:

```json
{
  "shard_id": "shard_0001",
  "sequences": [
    [3, 4, 5, 1],
    [6, 4, 7, 1]
  ]
}
```

The shard should be immutable: once created, do not modify it. If data changes, create a new shard with a new hash.

---

## 8. Manifest

A **manifest** is metadata about a shard. It tells you what is inside the shard and how it was produced.

Example:

```python
manifest = {
    "shard_id": "shard_0001",
    "token_count": 8,
    "document_ids": ["web_001", "web_002"],
    "language": "en",
    "data_type": "web",
    "tokenizer_hash": "abc123",
    "content_hash": "def456",
    "cleaning_hash": "clean789",
    "license": "demo",
    "curriculum_stage": "stage_1",
    "is_eval": False,
    "contamination_checked": True,
}
```

Minimum fields you should consider for the assignment:

- `shard_id`
- `document_ids`
- `token_count`
- `content_hash`
- `tokenizer_hash`
- `cleaning_hash`
- `data_type`
- `language`
- `curriculum_stage`
- `is_eval`

Content hash example:

```python
import hashlib, json

sequences = [[3, 4, 5, 1], [6, 4, 7, 1]]
content_hash = hashlib.sha256(
    json.dumps(sequences, sort_keys=True).encode()
).hexdigest()
```

---

## 9. Curriculum Stage

A **curriculum** decides what data the model sees at each stage.

Example:

```json
{
  "stage_1": {
    "description": "basic language and general web",
    "token_budget": 1000000,
    "lanes": {
      "web": 0.7,
      "indic": 0.2,
      "code": 0.1
    }
  },
  "stage_2": {
    "description": "code-heavy stage",
    "token_budget": 1000000,
    "lanes": {
      "web": 0.3,
      "indic": 0.2,
      "code": 0.5
    }
  }
}
```

Why it matters:

- Do not teach advanced code or agent traces too early.
- Keep protected flows like Indic data present throughout training.
- Use stages to control capability growth.

---

## 10. Lane Weights

A **lane** is a data category/capability bucket, such as:

- web
- code
- Indic
- science
- LaTeX
- agentic traces
- GK

Lane weights decide mixture proportions.

```python
lane_weights = {
    "web": 0.50,
    "code": 0.20,
    "indic": 0.20,
    "agentic": 0.10,
}
```

If a batch has 10 samples, a simple scheduler might choose:

```text
5 web samples
2 code samples
2 Indic samples
1 agentic sample
```

Simple sampling example:

```python
import random

lanes = ["web", "code", "indic", "agentic"]
weights = [0.5, 0.2, 0.2, 0.1]

chosen_lane = random.choices(lanes, weights=weights, k=1)[0]
print(chosen_lane)
```

For replay, do not rely only on re-running this random choice. Store the chosen lane in the ledger.

---

## 11. Protected Flow

A **protected flow** is data that must appear regularly even if another selection policy would reject it.

In the lecture, Indic data is a key example. The model should not “forget” Indic languages, so some Indic data should remain present across stages.

Example:

```python
protected_lanes = {
    "indic": 0.10,
    "agentic": 0.05,
}
```

Meaning:

- At least 10% Indic.
- At least 5% agentic traces.
- OPUS or another selector may reject data, but protected lanes may override rejection.

---

## 12. Annealing

**Annealing** means gradual transition between stages.

Bad transition:

```text
step 1-1000: only easy English
step 1001+: suddenly PhD English
```

Better transition:

```text
steps 1-800: mostly easy English
steps 801-1000: easy English + some PhD English
steps 1001-1200: PhD English + some easy English
```

Simple schedule:

```python
def linear_mix(step, start, end):
    if step <= start:
        return 0.0
    if step >= end:
        return 1.0
    return (step - start) / (end - start)

phd_weight = linear_mix(step=900, start=800, end=1200)
print(phd_weight)  # 0.25
```

---

## 13. OPUS Selection

In the lecture, **OPUS selection** is a data-selection strategy.

The idea:

1. Run a strong “gold/proxy” set through the model.
2. Identify weak weights/features that need updates.
3. Test candidate samples cheaply, maybe using only first 512 tokens.
4. Keep samples that update the needed parts.
5. Reject samples that do not help the current target.

Toy version:

```python
def opus_accept(sample_metadata):
    if sample_metadata["lane"] == "protected_indic":
        return True
    return sample_metadata["estimated_usefulness"] >= 0.7

samples = [
    {"id": "a", "lane": "web", "estimated_usefulness": 0.4},
    {"id": "b", "lane": "code", "estimated_usefulness": 0.9},
    {"id": "c", "lane": "protected_indic", "estimated_usefulness": 0.2},
]

accepted = [s for s in samples if opus_accept(s)]
print(accepted)
```

Important assignment point:

- Record OPUS decision in the ledger.
- Record whether a protected flow overrode rejection.

---

## 14. Packing

**Packing** means filling fixed-length training sequences with useful tokens.

Suppose:

```python
sequence_length = 8
docs = [
    [11, 12, 13],        # length 3
    [21, 22],            # length 2
    [31, 32, 33, 34],    # length 4
]
EOS = 1
PAD = 0
```

### Pad Only

Each document gets its own sequence.

```python
def pad_only(docs, seq_len, eos=1, pad=0):
    output = []
    for doc in docs:
        tokens = doc + [eos]
        tokens = tokens[:seq_len]
        tokens += [pad] * (seq_len - len(tokens))
        output.append(tokens)
    return output

print(pad_only(docs, 8))
```

Output:

```text
[
  [11, 12, 13, 1, 0, 0, 0, 0],
  [21, 22, 1, 0, 0, 0, 0, 0],
  [31, 32, 33, 34, 1, 0, 0, 0]
]
```

Pros:

- Simple.
- Preserves structure.

Cons:

- Wastes compute on PAD.

### Concatenate And Chop

Join documents with EOS and cut into fixed windows.

```python
def concat_and_chop(docs, seq_len, eos=1, pad=0):
    stream = []
    for doc in docs:
        stream.extend(doc + [eos])

    output = []
    for i in range(0, len(stream), seq_len):
        chunk = stream[i:i + seq_len]
        chunk += [pad] * (seq_len - len(chunk))
        output.append(chunk)
    return output

print(concat_and_chop(docs, 8))
```

Output:

```text
[
  [11, 12, 13, 1, 21, 22, 1, 31],
  [32, 33, 34, 1, 0, 0, 0, 0]
]
```

Pros:

- Better utilization.

Cons:

- Can chop a document in the middle.
- Bad for code/SFT/agentic traces if structure matters.

### Greedy Packing

Place documents into the current sequence until full, then start the next sequence.

```python
def greedy_pack(docs, seq_len, eos=1, pad=0):
    sequences = []
    current = []

    for doc in docs:
        item = doc + [eos]
        if len(current) + len(item) <= seq_len:
            current.extend(item)
        else:
            current += [pad] * (seq_len - len(current))
            sequences.append(current)
            current = item[:seq_len]

    if current:
        current += [pad] * (seq_len - len(current))
        sequences.append(current)

    return sequences
```

Pros:

- Fast.
- Usually good enough for large datasets.

Cons:

- Some holes remain.

### Best-Fit Packing

Try to place each document where it leaves the least unused space.

Toy implementation:

```python
def best_fit_pack(docs, seq_len, eos=1, pad=0):
    bins = []

    for doc in sorted(docs, key=len, reverse=True):
        item = doc + [eos]
        best_index = None
        best_remaining = None

        for i, bin_tokens in enumerate(bins):
            remaining = seq_len - len(bin_tokens)
            if len(item) <= remaining:
                new_remaining = remaining - len(item)
                if best_remaining is None or new_remaining < best_remaining:
                    best_index = i
                    best_remaining = new_remaining

        if best_index is None:
            bins.append(item[:seq_len])
        else:
            bins[best_index].extend(item)

    return [b + [pad] * (seq_len - len(b)) for b in bins]
```

Pros:

- Better packing efficiency.

Cons:

- More preprocessing cost.

### Structure-Preserving Packing

For agent traces, SFT conversations, or code files, you may not want unrelated examples mixed together.

Example:

```python
def structure_preserving_pack(trace, seq_len, eos=1, pad=0):
    tokens = trace + [eos]
    tokens = tokens[:seq_len]
    tokens += [pad] * (seq_len - len(tokens))
    return tokens
```

Use this when:

- Conversation turns must stay together.
- Tool calls and responses must stay together.
- Code should not be chopped in a damaging place.

---

## 15. Packing Utilization

**Packing utilization** measures how much of a sequence contains useful non-PAD tokens.

```python
def packing_utilization(sequence, pad_id=0):
    useful = sum(1 for token in sequence if token != pad_id)
    return useful / len(sequence)

seq = [11, 12, 13, 1, 0, 0, 0, 0]
print(packing_utilization(seq))  # 0.5
```

You should log this because padding wastes GPU money.

---

## 16. Loss Mask

A **loss mask** says which tokens should contribute to loss.

For normal pretraining:

```text
Input:  India is great <EOS>
Loss:   yes   yes yes   yes
```

For SFT:

```text
User: write a poem
Assistant: roses are red
```

Usually only assistant tokens receive loss:

```text
User tokens:      loss_mask = 0
Assistant tokens: loss_mask = 1
PAD tokens:       loss_mask = 0
```

Example:

```python
tokens =     [10, 11, 12, 20, 21, 22, 1, 0]
roles =      ["user", "user", "user", "assistant", "assistant", "assistant", "eos", "pad"]
loss_mask = [0, 0, 0, 1, 1, 1, 1, 0]
```

Function:

```python
def make_loss_mask(roles):
    return [1 if role in {"assistant", "eos"} else 0 for role in roles]
```

Why it matters:

- We do not want the model trained to predict user prompts as the answer.
- We want it trained to produce the assistant response.

---

## 17. Attention Mask

An **attention mask** controls which previous tokens the model can look at.

For causal language modeling, token `i` can attend to tokens `0..i`, not future tokens.

Tiny causal mask:

```python
def causal_attention_mask(n):
    return [[1 if j <= i else 0 for j in range(n)] for i in range(n)]

for row in causal_attention_mask(4):
    print(row)
```

Output:

```text
[1, 0, 0, 0]
[1, 1, 0, 0]
[1, 1, 1, 0]
[1, 1, 1, 1]
```

With PAD tokens, you usually also prevent attention to PAD:

```python
def pad_attention_mask(tokens, pad_id=0):
    return [1 if token != pad_id else 0 for token in tokens]

tokens = [11, 12, 1, 0, 0]
print(pad_attention_mask(tokens))  # [1, 1, 1, 0, 0]
```

---

## 18. Position IDs

**Position IDs** tell the model token order.

```python
tokens = [11, 12, 13, 1, 0, 0]
position_ids = [0, 1, 2, 3, 0, 0]
```

Simple function:

```python
def make_position_ids(tokens, pad_id=0):
    positions = []
    pos = 0
    for token in tokens:
        if token == pad_id:
            positions.append(0)
        else:
            positions.append(pos)
            pos += 1
    return positions
```

Why it matters:

- The model needs to know token order.
- For packed examples, position policy must be consistent.

---

## 19. Microbatch

A **microbatch** is the batch sent to one GPU.

Example:

```python
microbatch = [
    [11, 12, 13, 1, 0, 0, 0, 0],
    [21, 22, 1, 0, 0, 0, 0, 0],
]
```

If microbatch size is 2 and sequence length is 8:

```text
shape = [2, 8]
```

---

## 20. Global Batch

A **global batch** is the total batch across GPUs and gradient accumulation.

Formula:

```text
global_batch_tokens =
  num_gpus * microbatch_size * sequence_length * gradient_accumulation_steps
```

Example:

```python
num_gpus = 8
microbatch_size = 4
sequence_length = 4096
grad_accum = 4

global_batch_tokens = num_gpus * microbatch_size * sequence_length * grad_accum
print(global_batch_tokens)  # 524288
```

The lecture says large LLM training often wants very large global batches, sometimes around hundreds of thousands to a million tokens.

---

## 21. Gradient Accumulation

**Gradient accumulation** means doing several forward/backward passes before one optimizer update.

Why:

- GPU memory may not fit the desired global batch.
- Accumulation simulates a larger batch.

Toy example:

```python
grad_accum_steps = 4
accumulated_loss = 0

for i in range(grad_accum_steps):
    loss = fake_forward_backward(i)
    accumulated_loss += loss

optimizer_step_loss = accumulated_loss / grad_accum_steps
print("optimizer update with loss", optimizer_step_loss)
```

Fake function:

```python
def fake_forward_backward(i):
    return 1.0 / (i + 1)
```

Training step means one optimizer update, not every micro-step.

---

## 22. Checkpoint

A **checkpoint** saves training state so you can resume later.

Real checkpoint may include:

- model weights
- optimizer state
- scheduler state
- RNG state
- data loader position
- ledger offset

Assignment checkpoint can be simpler:

```json
{
  "global_step": 120,
  "ledger_offset": 120,
  "current_shard": "shard_0007",
  "rng_seed": 42
}
```

Example:

```python
import json

checkpoint = {
    "global_step": 10,
    "ledger_offset": 10,
    "rng_seed": 123,
}

with open("checkpoint.json", "w") as f:
    json.dump(checkpoint, f, indent=2)
```

---

## 23. Crash And Resume

Your assignment should simulate a crash.

Example:

```python
def train(max_steps, crash_at=None):
    for step in range(max_steps):
        if crash_at is not None and step == crash_at:
            raise RuntimeError("simulated crash")
        print("training step", step)

try:
    train(max_steps=10, crash_at=5)
except RuntimeError:
    print("crashed; now resume from checkpoint")
```

Resume should use the checkpoint and ledger:

```python
def resume_from_checkpoint(checkpoint):
    start_step = checkpoint["global_step"]
    print("resuming from", start_step)
```

Important:

- Do not restart from step 0.
- Do not randomly reshuffle data.
- Resume from the exact ledger offset.

---

## 24. Replay

**Replay** means reusing the ledger as the source of truth.

If the first run consumed:

```text
step 0 -> shard_001 sample_004
step 1 -> shard_003 sample_010
step 2 -> shard_002 sample_001
```

Replay must consume the same sequence:

```text
step 0 -> shard_001 sample_004
step 1 -> shard_003 sample_010
step 2 -> shard_002 sample_001
```

Do not recompute random selection during replay. Read the ledger.

Ledger record example:

```json
{
  "run_id": "run_001",
  "global_step": 2,
  "shard_id": "shard_002",
  "sample_index": 1,
  "curriculum_stage": "stage_1",
  "lane": "indic",
  "opus_decision": "accepted",
  "protected_override": false,
  "token_count": 4096,
  "loss": 2.91
}
```

---

## 25. Data Ledger

The **data ledger** is the most important concept in the lecture.

It records what was consumed during training and what happened.

It should answer:

- Which shard was used?
- Which sample was used?
- At which global step?
- In which curriculum stage?
- Which lane?
- What tokenizer?
- What packing policy?
- What loss mask?
- What attention/position policy?
- Was OPUS used?
- Was there a protected override?
- What was the fake loss?
- Which checkpoint can resume from this point?

Example JSONL ledger:

```jsonl
{"global_step":0,"shard_id":"shard_0001","sample_index":0,"lane":"web","loss":3.1}
{"global_step":1,"shard_id":"shard_0001","sample_index":1,"lane":"code","loss":2.8}
{"global_step":2,"shard_id":"shard_0002","sample_index":0,"lane":"indic","loss":4.2}
```

Writing JSONL:

```python
import json

def append_ledger(path, record):
    with open(path, "a") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")
```

Reading JSONL:

```python
def read_ledger(path):
    with open(path) as f:
        return [json.loads(line) for line in f]
```

---

## 26. Loss And Perplexity

**Loss** measures how wrong the model was when predicting the next token.

**Perplexity** is:

```text
perplexity = exp(loss)
```

Toy example:

```python
import math

loss = 2.0
perplexity = math.exp(loss)
print(perplexity)  # 7.389...
```

Interpretation:

- High loss/perplexity: model is surprised; it does not know this well.
- Low loss/perplexity: model predicts it easily.
- Extremely low loss may indicate repetitive/boring/contaminated data.

Why token-level loss matters:

```text
sample average loss = 2.0
but:
first half loss = 0.3
second half loss = 4.6
```

The average hides important structure. Token-level loss helps identify which part of the sample mattered.

Fake token loss:

```python
def fake_token_losses(tokens, pad_id=0):
    losses = []
    for token in tokens:
        if token == pad_id:
            losses.append(0.0)
        else:
            losses.append((token % 10) / 10 + 1.0)
    return losses
```

---

## 27. Evaluation Firewall

An **evaluation firewall** prevents training on evaluation/test data.

Manifest field:

```json
{
  "shard_id": "shard_eval_001",
  "is_eval": true
}
```

Training loader should reject eval shards:

```python
def can_train_on_shard(manifest):
    return not manifest["is_eval"]
```

Why it matters:

- If eval data leaks into training, benchmark scores become fake.
- The lecture compares this to exam paper leakage.

---

## 28. Contamination

**Contamination** means training data overlaps with benchmark/test data or contains data that should not be used.

Example manifest fields:

```json
{
  "contamination_checked": true,
  "eval_overlap": false,
  "pii_removed": true
}
```

Assignment version:

- You can simulate this with metadata.
- Show that your loader skips contaminated/eval shards.

---

## 29. Fake Training Loop

For the assignment, fake training is enough.

Example:

```python
def fake_train_step(batch):
    token_count = sum(len(sample["tokens"]) for sample in batch)
    useful_tokens = sum(
        sum(sample["loss_mask"]) for sample in batch
    )
    fake_loss = token_count / max(useful_tokens, 1)
    return {
        "token_count": token_count,
        "useful_tokens": useful_tokens,
        "loss": fake_loss,
    }
```

Purpose:

- Prove batches are consumed.
- Prove ledger is written.
- Prove checkpoint/resume works.
- Prove replay uses same order.

---

## 30. End-To-End Mini Design

Suggested folder structure:

```text
session6_assignment/
  README.md
  run_demo.py
  data/
    raw_docs.jsonl
  artifacts/
    tokenizer.json
    shards/
      shard_0001.json
      shard_0001.manifest.json
    checkpoints/
      checkpoint_step_0003.json
    log.jsonl
    evidence.md
```

Suggested pipeline:

```python
def main():
    docs = load_raw_docs()
    cleaned = clean_docs(docs)
    tokenizer = load_or_create_frozen_tokenizer(cleaned)
    tokenized = tokenize_docs(cleaned, tokenizer)
    shards = create_immutable_shards(tokenized)
    manifests = write_manifests(shards)
    schedule = load_curriculum_schedule()
    batches = build_batches(shards, manifests, schedule)
    run_fake_training_with_crash_resume_replay(batches)
    write_evidence()
```

---

## 31. What Your Assignment Must Prove

Your `evidence.md` should clearly show:

```text
1. Tokenizer hash is stable.
2. Shard content hash is stable.
3. Eval shards were not trained on.
4. Packing policy was applied.
5. Loss mask, attention mask, and position IDs exist.
6. Ledger records every consumed batch/sample.
7. Crash happened intentionally.
8. Resume continued from checkpoint/ledger offset.
9. Replay used the same shard/sample order.
10. Final run completed.
```

Example evidence:

```md
# Evidence

- Frozen tokenizer hash: `abc123`
- Created 3 train shards and 1 eval shard.
- Eval shard skipped: `shard_eval_001`
- Packing policies used:
  - web: greedy
  - code: structure_preserving
  - agentic: structure_preserving
- Simulated crash at global step 3.
- Resumed from checkpoint step 3.
- Replay matched original ledger order: yes.
```

---

## 32. Common Mistakes

Avoid these:

- Changing tokenizer after shard creation.
- Not storing content hashes.
- Training on eval/test shards.
- Recomputing random order during replay.
- Not recording OPUS/protected decisions.
- Padding everything and ignoring utilization.
- Forgetting loss masks for SFT/agentic data.
- Treating checkpoint as only model weights.
- Resuming from approximate step instead of exact ledger offset.
- Building only a tokenizer instead of the full ledger path.

---

## 33. Mental Model

Think of the ledger like a bank statement for training data.

The trainer asks:

```text
What should I train on now?
```

The data system replies:

```text
Use shard_0007, sample 42, packed with greedy policy,
stage code_heavy, lane code, tokenizer hash abc123.
```

After training, the ledger records:

```text
At step 1402, this exact sample was consumed,
with this loss, this mask policy, and this checkpoint state.
```

If training crashes, you do not guess. You read the ledger and continue.

That is the core idea of Session 6.
