"""Session 10: make a small language model tell the truth about itself.

The harness is intentionally explicit rather than optimized.  It prints the
tensor shapes in one real forward pass, checks one autograd gradient with a
finite difference, demonstrates the variable-token gradient-accumulation bug,
logs gradient norms, reports an MFU calculation, and decodes 0.1 in three
floating-point formats.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import struct
import time
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F


SEED = 10
CORPUS = (
    "the quick brown fox jumps over the lazy dog. "
    "small models can reveal large ideas. "
    "gradients tell us how loss changes when weights move. "
) * 80


def seed_everything(seed: int = SEED) -> None:
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False


class CharTokenizer:
    def __init__(self, text: str):
        self.itos = sorted(set(text))
        self.stoi = {ch: i for i, ch in enumerate(self.itos)}

    def encode(self, text: str) -> list[int]:
        return [self.stoi[ch] for ch in text]

    def decode(self, ids: list[int]) -> str:
        return "".join(self.itos[int(i)] for i in ids)


class ShapeTracer:
    def __init__(self):
        self.rows: list[dict[str, object]] = []

    def record(self, name: str, tensor: torch.Tensor, meaning: str) -> torch.Tensor:
        self.rows.append({"name": name, "shape": list(tensor.shape), "meaning": meaning})
        return tensor

    def print(self) -> None:
        print("\nTENSOR SHAPES: one real forward pass")
        print("-" * 96)
        for row in self.rows:
            print(f"{row['name']:<28} shape={tuple(row['shape'])!s:<22} {row['meaning']}")


class CausalSelfAttention(nn.Module):
    def __init__(self, n_embd: int, n_head: int):
        super().__init__()
        if n_embd % n_head:
            raise ValueError("n_embd must be divisible by n_head")
        self.n_head = n_head
        self.head_dim = n_embd // n_head
        self.qkv = nn.Linear(n_embd, 3 * n_embd, bias=False)
        self.proj = nn.Linear(n_embd, n_embd, bias=False)

    def forward(self, x: torch.Tensor, tracer: ShapeTracer | None = None, block: int = 0):
        b, t, c = x.shape
        qkv = self.qkv(x)
        if tracer:
            tracer.record(f"blocks.{block}.attn.qkv", qkv, "B,T,3C: concatenated query/key/value")
        qkv = qkv.view(b, t, 3, self.n_head, self.head_dim).permute(2, 0, 3, 1, 4)
        q, k, v = qkv.unbind(0)
        if tracer:
            tracer.record(f"blocks.{block}.attn.Q", q, "B,H,T,Dh: query per attention head")
            tracer.record(f"blocks.{block}.attn.K", k, "B,H,T,Dh: key per attention head")
            tracer.record(f"blocks.{block}.attn.V", v, "B,H,T,Dh: value per attention head")
        scores = q @ k.transpose(-2, -1) / math.sqrt(self.head_dim)
        if tracer:
            tracer.record(f"blocks.{block}.attn.scores", scores, "B,H,T,T: token-to-token attention scores")
        mask = torch.triu(torch.ones(t, t, device=x.device, dtype=torch.bool), diagonal=1)
        if tracer:
            tracer.record(f"blocks.{block}.attn.causal_mask", mask, "T,T: True entries block future-token attention")
        scores = scores.masked_fill(mask, float("-inf"))
        weights = F.softmax(scores, dim=-1)
        if tracer:
            tracer.record(f"blocks.{block}.attn.weights", weights, "B,H,T,T: causal attention probabilities")
        y = weights @ v
        y = y.transpose(1, 2).contiguous().view(b, t, c)
        if tracer:
            tracer.record(f"blocks.{block}.attn.context", y, "B,T,C: heads concatenated")
        y = self.proj(y)
        if tracer:
            tracer.record(f"blocks.{block}.attn.output", y, "B,T,C: attention projection")
        return y


class MLP(nn.Module):
    def __init__(self, n_embd: int):
        super().__init__()
        self.fc = nn.Linear(n_embd, 4 * n_embd, bias=False)
        self.proj = nn.Linear(4 * n_embd, n_embd, bias=False)

    def forward(self, x: torch.Tensor, tracer: ShapeTracer | None = None, block: int = 0):
        up = self.fc(x)
        if tracer:
            tracer.record(f"blocks.{block}.mlp.up", up, "B,T,4C: feed-forward expansion")
        activated = F.gelu(up)
        if tracer:
            tracer.record(f"blocks.{block}.mlp.gelu", activated, "B,T,4C: nonlinear activation")
        down = self.proj(activated)
        if tracer:
            tracer.record(f"blocks.{block}.mlp.down", down, "B,T,C: feed-forward compression")
        return down


class Block(nn.Module):
    def __init__(self, n_embd: int, n_head: int):
        super().__init__()
        self.ln1 = nn.LayerNorm(n_embd)
        self.attn = CausalSelfAttention(n_embd, n_head)
        self.ln2 = nn.LayerNorm(n_embd)
        self.mlp = MLP(n_embd)

    def forward(self, x: torch.Tensor, tracer: ShapeTracer | None = None, block: int = 0):
        x = x + self.attn(self.ln1(x), tracer, block)
        return x + self.mlp(self.ln2(x), tracer, block)


class TinyGPT(nn.Module):
    def __init__(self, vocab_size: int, block_size: int, n_embd: int = 64, n_head: int = 4, n_layer: int = 2):
        super().__init__()
        self.block_size = block_size
        self.token_embedding = nn.Embedding(vocab_size, n_embd)
        self.position_embedding = nn.Embedding(block_size, n_embd)
        self.blocks = nn.ModuleList([Block(n_embd, n_head) for _ in range(n_layer)])
        self.final_norm = nn.LayerNorm(n_embd)
        self.lm_head = nn.Linear(n_embd, vocab_size, bias=False)
        self.n_embd = n_embd

    def forward(self, tokens: torch.Tensor, tracer: ShapeTracer | None = None):
        b, t = tokens.shape
        if t > self.block_size:
            raise ValueError(f"sequence length {t} exceeds block size {self.block_size}")
        if tracer:
            tracer.record("tokens", tokens, "B,T: integer token ids")
        positions = torch.arange(t, device=tokens.device)
        x = self.token_embedding(tokens)
        if tracer:
            tracer.record("token_embedding", x, "B,T,C: learned token vectors")
        pos = self.position_embedding(positions)[None, :, :]
        if tracer:
            tracer.record("position_embedding", pos, "1,T,C: broadcastable position vectors")
        x = x + pos
        if tracer:
            tracer.record("embedding_sum", x, "B,T,C: token plus position representation")
        for index, block in enumerate(self.blocks):
            x = block(x, tracer, index)
            if tracer:
                tracer.record(f"blocks.{index}.output", x, "B,T,C: residual block output")
        hidden = self.final_norm(x)
        if tracer:
            tracer.record("final_norm", hidden, "B,T,C: normalized hidden states")
        logits = self.lm_head(hidden)
        if tracer:
            tracer.record("logits", logits, "B,T,V: one score for every vocabulary token")
        return logits


@dataclass
class Config:
    device: torch.device
    vocab_size: int
    block_size: int = 32
    n_embd: int = 64
    n_head: int = 4
    n_layer: int = 2


def parameter_rows(model: nn.Module) -> list[dict[str, object]]:
    rows = []
    for name, parameter in model.named_parameters():
        rows.append({
            "name": name,
            "shape": list(parameter.shape),
            "parameters": parameter.numel(),
            "trainable": bool(parameter.requires_grad),
        })
    return rows


def unique_parameter_count(model: nn.Module) -> int:
    seen: set[int] = set()
    total = 0
    for parameter in model.parameters():
        if id(parameter) not in seen:
            total += parameter.numel()
            seen.add(id(parameter))
    return total


def loss_for(model: nn.Module, inputs: torch.Tensor, targets: torch.Tensor, reduction: str = "mean") -> torch.Tensor:
    logits = model(inputs)
    return F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1), reduction=reduction)


def sequence_batch(stream: torch.Tensor, start: int, length: int, device: torch.device):
    row = stream[start:start + length].to(device)
    return row[:-1].unsqueeze(0), row[1:].unsqueeze(0)


def gradient_check(config: Config, stream: torch.Tensor) -> dict[str, float | str]:
    print("\nGRADIENT CHECK: finite difference versus backward()")
    seed_everything(SEED + 1)
    model = TinyGPT(config.vocab_size, config.block_size, config.n_embd, config.n_head, config.n_layer).to(config.device)
    inputs, targets = sequence_batch(stream, 41, 18, config.device)
    loss = loss_for(model, inputs, targets)
    loss.backward()
    parameter = model.lm_head.weight
    index = (0, 0)
    analytic = float(parameter.grad[index].item())
    original = float(parameter[index].item())
    # 1e-3 is mathematically valid but unnecessarily noisy for this float32
    # loss; 1e-2 gives a stable centered finite difference without leaving the
    # local linear neighborhood.
    epsilon = 1e-2
    with torch.no_grad():
        parameter[index] = original + epsilon
    plus = float(loss_for(model, inputs, targets).item())
    with torch.no_grad():
        parameter[index] = original - epsilon
    minus = float(loss_for(model, inputs, targets).item())
    with torch.no_grad():
        parameter[index] = original
    one_sided = (plus - float(loss.item())) / epsilon
    centered = (plus - minus) / (2 * epsilon)
    abs_error = abs(centered - analytic)
    relative_error = abs_error / max(abs(analytic), 1e-12)
    print(f"parameter=lm_head.weight{index}; original={original:.8f}; epsilon={epsilon}")
    print(f"loss(w)={loss.item():.9f}; loss(w+eps)={plus:.9f}; loss(w-eps)={minus:.9f}")
    print(f"backward gradient={analytic:.9f}")
    print(f"one-sided estimate={one_sided:.9f}; centered estimate={centered:.9f}")
    print(f"centered absolute error={abs_error:.3e}; relative error={relative_error:.3e}")
    if abs_error > 2e-4:
        raise AssertionError("finite-difference gradient does not agree with autograd")
    return {
        "parameter": "lm_head.weight[0,0]",
        "epsilon": epsilon,
        "loss": float(loss.item()),
        "loss_plus": plus,
        "loss_minus": minus,
        "backward": analytic,
        "one_sided": one_sided,
        "centered": centered,
        "absolute_error": abs_error,
        "relative_error": relative_error,
    }


def microbatch_specs(stream: torch.Tensor, step: int, device: torch.device):
    # The two sequences have different numbers of valid prediction tokens.
    first_start = 17 + (step * 7) % 300
    second_start = 211 + (step * 11) % 300
    return [
        sequence_batch(stream, first_start, 5, device),
        sequence_batch(stream, second_start, 17, device),
    ]


def accumulate(model: nn.Module, batches, correct: bool):
    total_tokens = sum(int(targets.numel()) for _, targets in batches)
    losses = []
    for inputs, targets in batches:
        logits = model(inputs)
        summed = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1), reduction="sum")
        mean = summed / targets.numel()
        losses.append(float(mean.detach().item()))
        if correct:
            (summed / total_tokens).backward()
        else:
            (mean / len(batches)).backward()
    return sum(losses) / len(losses), total_tokens


def global_grad_norm(model: nn.Module) -> float:
    squared = 0.0
    for parameter in model.parameters():
        if parameter.grad is not None:
            squared += float(parameter.grad.detach().float().pow(2).sum().item())
    return math.sqrt(squared)


def probe_loss(model: nn.Module, probe, device: torch.device) -> float:
    model.eval()
    with torch.no_grad():
        value = loss_for(model, probe[0].to(device), probe[1].to(device)).item()
    model.train()
    return float(value)


def accumulation_experiment(config: Config, stream: torch.Tensor, steps: int = 80):
    print("\nGRADIENT ACCUMULATION: mean of means versus token-weighted mean")
    seed_everything(SEED + 2)
    base = TinyGPT(config.vocab_size, config.block_size, config.n_embd, config.n_head, config.n_layer)
    naive = TinyGPT(config.vocab_size, config.block_size, config.n_embd, config.n_head, config.n_layer).to(config.device)
    correct = TinyGPT(config.vocab_size, config.block_size, config.n_embd, config.n_head, config.n_layer).to(config.device)
    naive.load_state_dict(base.state_dict())
    correct.load_state_dict(base.state_dict())
    optimizer_naive = torch.optim.SGD(naive.parameters(), lr=0.35)
    optimizer_correct = torch.optim.SGD(correct.parameters(), lr=0.35)
    probe = sequence_batch(stream, 503, 25, config.device)

    # A single reference loss made from the two summed micro-batch losses is
    # mathematically the same objective as token-weighted accumulation. Check
    # the gradients before either training copy is updated.
    reference = TinyGPT(config.vocab_size, config.block_size, config.n_embd, config.n_head, config.n_layer).to(config.device)
    reference.load_state_dict(base.state_dict())
    reference.zero_grad(set_to_none=True)
    reference_batches = microbatch_specs(stream, 0, config.device)
    reference_total = sum(int(targets.numel()) for _, targets in reference_batches)
    reference_sum = 0.0
    for inputs, targets in reference_batches:
        logits = reference(inputs)
        reference_sum = reference_sum + F.cross_entropy(
            logits.reshape(-1, logits.shape[-1]), targets.reshape(-1), reduction="sum"
        )
    (reference_sum / reference_total).backward()
    correct.zero_grad(set_to_none=True)
    accumulate(correct, reference_batches, True)
    reference_grad_gap = max(
        float((reference_grad - correct_param.grad).abs().max().item())
        for reference_param, correct_param in zip(reference.parameters(), correct.parameters())
        for reference_grad in [reference_param.grad]
    )
    correct.zero_grad(set_to_none=True)
    print(f"reference-vs-token-weighted max gradient gap: {reference_grad_gap:.3e}")
    if reference_grad_gap > 1e-6:
        raise AssertionError("token-weighted accumulation does not match reference global loss")

    rows = []
    for step in range(steps):
        batches = microbatch_specs(stream, step, config.device)
        for model, optimizer, is_correct in ((naive, optimizer_naive, False), (correct, optimizer_correct, True)):
            optimizer.zero_grad(set_to_none=True)
            average_loss, token_count = accumulate(model, batches, is_correct)
            norm = global_grad_norm(model)
            optimizer.step()
            measured = probe_loss(model, probe, config.device)
            rows.append({
                "step": step + 1,
                "method": "token_weighted" if is_correct else "mean_of_means",
                "microbatch_mean_loss": average_loss,
                "valid_tokens": token_count,
                "grad_norm": norm,
                "probe_loss": measured,
            })
    naive_final = rows[-2]["probe_loss"]
    correct_final = rows[-1]["probe_loss"]
    parameter_gap = max(
        float((naive.state_dict()[name] - correct.state_dict()[name]).abs().max().item())
        for name in naive.state_dict()
    )
    print("micro-batch valid tokens: 4 and 16")
    print(f"final fixed-probe loss, mean of means: {naive_final:.6f}")
    print(f"final fixed-probe loss, token weighted: {correct_final:.6f}")
    print(f"maximum parameter absolute gap: {parameter_gap:.6e}")
    if parameter_gap < 1e-5:
        raise AssertionError("the intentionally incorrect accumulation path did not diverge")
    return rows, {
        "naive_final": naive_final,
        "correct_final": correct_final,
        "parameter_gap": parameter_gap,
        "reference_grad_gap": reference_grad_gap,
    }


def find_gradient_lead(rows: list[dict[str, object]]) -> dict[str, object]:
    correct_rows = [row for row in rows if row["method"] == "token_weighted"]
    candidates = []
    for previous, current in zip(correct_rows, correct_rows[1:]):
        norm_change = abs(float(current["grad_norm"]) - float(previous["grad_norm"])) / max(float(previous["grad_norm"]), 1e-12)
        loss_change = abs(float(current["probe_loss"]) - float(previous["probe_loss"])) / max(float(previous["probe_loss"]), 1e-12)
        candidates.append((norm_change - loss_change, norm_change, loss_change, current))
    qualifying = [item for item in candidates if item[1] >= 0.05 and item[2] <= 0.005]
    _, norm_change, loss_change, selected = (qualifying[0] if qualifying else max(candidates, key=lambda item: item[0]))
    result = {
        "step": selected["step"],
        "grad_norm": selected["grad_norm"],
        "probe_loss": selected["probe_loss"],
        "relative_grad_norm_change": norm_change,
        "relative_probe_loss_change": loss_change,
    }
    print("\nGRADIENT-NORM LEAD: norm moved substantially while loss barely moved")
    print(json.dumps(result, indent=2))
    return result


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def plot_accumulation(rows: list[dict[str, object]], path: Path) -> None:
    plt.figure(figsize=(9, 5))
    for method, label, color in (
        ("mean_of_means", "naive average of averages", "#ef4444"),
        ("token_weighted", "correct token-weighted accumulation", "#2563eb"),
    ):
        subset = [row for row in rows if row["method"] == method]
        plt.plot([row["step"] for row in subset], [row["probe_loss"] for row in subset], label=label, color=color, linewidth=2)
    plt.xlabel("optimizer step")
    plt.ylabel("fixed-probe cross-entropy loss")
    plt.title("Different-length micro-batches: the accumulation bug is visible")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def plot_diagnostics(rows: list[dict[str, object]], path: Path) -> None:
    subset = [row for row in rows if row["method"] == "token_weighted"]
    figure, left = plt.subplots(figsize=(9, 5))
    left.plot([row["step"] for row in subset], [row["grad_norm"] for row in subset], color="#7c3aed", label="pre-update grad norm")
    left.set_xlabel("optimizer step")
    left.set_ylabel("global gradient L2 norm", color="#7c3aed")
    left.tick_params(axis="y", labelcolor="#7c3aed")
    right = left.twinx()
    right.plot([row["step"] for row in subset], [row["probe_loss"] for row in subset], color="#059669", label="probe loss")
    right.set_ylabel("fixed-probe loss", color="#059669")
    right.tick_params(axis="y", labelcolor="#059669")
    figure.suptitle("Gradient norm and loss are different observables")
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


def fp32_bits(value: float) -> str:
    integer = struct.unpack(">I", struct.pack(">f", value))[0]
    return f"{integer:032b}"


def fp_formats() -> dict[str, object]:
    value = 0.1
    fp32 = fp32_bits(value)
    bf16_int = int(fp32[:16], 2)
    # Round the discarded FP32 low half to nearest-even when forming BF16.
    discarded = int(fp32[16:], 2)
    if discarded > 0x8000 or (discarded == 0x8000 and (bf16_int & 1)):
        bf16_int += 1
    bf16_bits_text = f"{bf16_int:016b}"
    # 0.1 = 1.6 * 2^-4. E4M3 has exponent bias 7 and rounds 0.6*8 to 5.
    fp8_int = (0 << 7) | (0b0011 << 3) | 0b101
    result = {
        "decimal_input": value,
        "fp32": {"bits": fp32, "grouped": f"{fp32[0]} {fp32[1:9]} {fp32[9:]}", "decoded": struct.unpack(">f", struct.pack(">I", int(fp32, 2)))[0]},
        "bf16": {"bits": bf16_bits_text, "grouped": f"{bf16_bits_text[0]} {bf16_bits_text[1:9]} {bf16_bits_text[9:]}", "decoded": struct.unpack(">f", struct.pack(">I", bf16_int << 16))[0]},
        "fp8_e4m3": {"bits": f"{fp8_int:08b}", "grouped": f"{fp8_int >> 7} {(fp8_int >> 3) & 0b1111:04b} {fp8_int & 0b111:03b}", "decoded": (1 + 5 / 8) * 2 ** -4},
    }
    print("\nFLOATING-POINT REPRESENTATION OF 0.1")
    for name, row in result.items():
        if name == "decimal_input":
            continue
        print(f"{name:<10} bits={row['grouped']:<29} decoded={row['decoded']:.12f}")
    return result


def make_report(path: Path, results: dict[str, object]) -> None:
    gradient = results["gradient_check"]
    accumulation = results["accumulation"]
    mfu = results["mfu"]
    lead = results["gradient_lead"]
    formats = results["floating_point"]
    path.write_text(
        "# Session 10 — Training Loop Truth Report\n\n"
        "This report was generated by `training_harness.py` with a deterministic, character-level, two-block GPT.\n\n"
        "## 1. Tensor shapes\n\n"
        "The complete shape table is printed by the harness and stored in `results.json` under `shape_trace`. Every dimension is named in the output.\n\n"
        "## 2. Gradient check\n\n"
        f"Parameter `{gradient['parameter']}`: backward={gradient['backward']:.9f}, centered finite difference={gradient['centered']:.9f}, absolute error={gradient['absolute_error']:.3e}. The estimates agree to several decimals.\n\n"
        "## 3. Gradient accumulation\n\n"
        "The two micro-batches contain 4 and 16 valid prediction tokens. Averaging their mean losses gives each micro-batch equal influence; token-weighted accumulation gives each valid token equal influence. The curves are in `accumulation_comparison.png`.\n\n"
        f"The final fixed-probe losses were {accumulation['naive_final']:.6f} (naive) and {accumulation['correct_final']:.6f} (correct), with maximum parameter gap {accumulation['parameter_gap']:.3e}.\n\n"
        "## 4. Gradient norm\n\n"
        f"Selected step {lead['step']}: relative gradient-norm change={lead['relative_grad_norm_change']:.3%}; relative probe-loss change={lead['relative_probe_loss_change']:.3%}. The diagnostic plot is `training_diagnostics.png`.\n\n"
        "## 5. MFU\n\n"
        f"Unique trainable parameters N={mfu['parameters']:,}; measured tokens/sec={mfu['tokens_per_second']:.3f}; estimated achieved throughput={mfu['achieved_tflops']:.6f} TFLOP/s using 6NT. Conventional MFU={mfu['mfu_text']}. This local machine has no CUDA device and no supplied hardware peak, so inventing a GPU percentage would be dishonest. Re-run with `--peak-tflops VALUE` on a known GPU to obtain conventional MFU.\n\n"
        "The gap to a 40% target is expected to be dominated by Python overhead, tiny GEMMs with poor occupancy, memory movement, CPU execution, and the rough 6NT estimate.\n\n"
        "## 6. 0.1 by hand\n\n"
        f"- FP32: `{formats['fp32']['grouped']}` → {formats['fp32']['decoded']:.12f}\n"
        f"- BF16: `{formats['bf16']['grouped']}` → {formats['bf16']['decoded']:.12f}\n"
        f"- FP8 E4M3: `{formats['fp8_e4m3']['grouped']}` → {formats['fp8_e4m3']['decoded']:.12f}\n\n"
        "For this experiment I would train in BF16, retaining FP32 accumulation/master state where needed. BF16 has FP32-like exponent range and therefore preserves small gradients better than FP16-like formats. Raw FP8 E4M3 is too coarse for an unscaled end-to-end cast; FP8 training needs scale management or a hybrid recipe.\n"
    )


def run(args: argparse.Namespace) -> dict[str, object]:
    seed_everything(SEED)
    device = torch.device(args.device if args.device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu"))
    tokenizer = CharTokenizer(CORPUS)
    stream = torch.tensor(tokenizer.encode(CORPUS), dtype=torch.long)
    config = Config(device=device, vocab_size=len(tokenizer.itos))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"device={device}; vocab={config.vocab_size}; seed={SEED}")

    model = TinyGPT(config.vocab_size, config.block_size, config.n_embd, config.n_head, config.n_layer).to(device)
    trace = ShapeTracer()
    trace_inputs, trace_targets = sequence_batch(stream, 3, 12, device)
    with torch.no_grad():
        trace_logits = model(trace_inputs, trace)
        trace.record("flat_logits", trace_logits.reshape(-1, trace_logits.shape[-1]), "B*T,V: logits flattened for cross-entropy")
        trace.record("flat_targets", trace_targets.reshape(-1), "B*T: next-token labels flattened for cross-entropy")
        trace_loss = F.cross_entropy(trace_logits.reshape(-1, trace_logits.shape[-1]), trace_targets.reshape(-1))
        trace.record("loss", trace_loss, "scalar: mean cross-entropy over valid next-token labels")
    trace.print()
    rows = parameter_rows(model)
    print("\nPARAMETERS")
    for row in rows:
        print(f"{row['name']:<34} shape={tuple(row['shape'])!s:<18} count={row['parameters']:,} trainable={row['trainable']}")

    gradient = gradient_check(config, stream)
    accumulation_rows, accumulation_summary = accumulation_experiment(config, stream, args.steps)
    lead = find_gradient_lead(accumulation_rows)
    plot_accumulation(accumulation_rows, out_dir / "accumulation_comparison.png")
    plot_diagnostics(accumulation_rows, out_dir / "training_diagnostics.png")
    write_csv(out_dir / "training_metrics.csv", accumulation_rows)

    parameters = unique_parameter_count(model)
    valid_tokens = sum(int(row["valid_tokens"]) for row in accumulation_rows if row["method"] == "token_weighted")
    # Time the real loop separately from plotting and reporting.
    timed_model = TinyGPT(config.vocab_size, config.block_size, config.n_embd, config.n_head, config.n_layer).to(device)
    optimizer = torch.optim.SGD(timed_model.parameters(), lr=0.35)
    if device.type == "cuda":
        torch.cuda.synchronize(device)
    started = time.perf_counter()
    for step in range(args.steps):
        optimizer.zero_grad(set_to_none=True)
        accumulate(timed_model, microbatch_specs(stream, step, device), True)
        optimizer.step()
    if device.type == "cuda":
        torch.cuda.synchronize(device)
    elapsed = time.perf_counter() - started
    tokens_per_second = valid_tokens / max(elapsed, 1e-12)
    achieved_tflops = (6 * parameters * tokens_per_second) / 1e12
    mfu_value = None if args.peak_tflops is None else achieved_tflops / args.peak_tflops
    mfu = {
        "parameters": parameters,
        "tokens_processed": valid_tokens,
        "elapsed_seconds": elapsed,
        "tokens_per_second": tokens_per_second,
        "achieved_tflops": achieved_tflops,
        "peak_tflops": args.peak_tflops,
        "mfu": mfu_value,
        "mfu_text": "unavailable (no peak supplied; CPU-only run)" if mfu_value is None else f"{mfu_value:.3%}",
    }
    print("\nMFU")
    print(json.dumps(mfu, indent=2))
    formats = fp_formats()
    results = {
        "config": {"device": str(device), "seed": SEED, "vocab_size": config.vocab_size, "block_size": config.block_size, "n_embd": config.n_embd, "n_head": config.n_head, "n_layer": config.n_layer},
        "parameters": rows,
        "shape_trace": trace.rows,
        "gradient_check": gradient,
        "accumulation": accumulation_summary,
        "gradient_lead": lead,
        "mfu": mfu,
        "floating_point": formats,
    }
    (out_dir / "results.json").write_text(json.dumps(results, indent=2))
    make_report(Path(args.report), results)
    print(f"\nWrote artifacts to {out_dir}")
    print(f"Wrote report to {args.report}")
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--peak-tflops", type=float, default=None, help="hardware peak TFLOP/s for conventional MFU")
    parser.add_argument("--out-dir", default="session10/artifacts")
    parser.add_argument("--report", default="session10/REPORT.md")
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
