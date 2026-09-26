"""Session 13 reversible language-model experiment.

The reversible variants implement midpoint and Hamiltonian symplectic-Euler
updates. Their custom backward passes reconstruct hidden states from the final
states, so intermediate layer activations are not retained for backpropagation.
"""

from __future__ import annotations

import argparse
import array
import csv
import gc
import hashlib
import json
import math
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.checkpoint import checkpoint


@dataclass(frozen=True)
class Config:
    vocab_size: int = 50_257
    context_length: int = 256
    d_model: int = 256
    n_heads: int = 8
    n_layers: int = 9
    ffn_multiple: int = 4
    step_size: float = 0.25
    train_tokens: int = 50_000_000
    validation_tokens: int = 250_000
    seed: int = 13
    learning_rate: float = 3e-4
    warmup_fraction: float = 0.02
    grad_clip: float = 1.0
    eval_interval: int = 200
    data_name: str = "HuggingFaceFW/fineweb-edu"
    data_config: str = "sample-10BT"
    tokenizer_name: str = "gpt2"

    def parameter_count(self) -> int:
        model = LanguageModel(self, "baseline")
        return sum(p.numel() for p in model.parameters() if p.requires_grad)

    def as_dict(self) -> dict:
        result = asdict(self)
        result["parameter_count"] = self.parameter_count()
        return result


class CausalSelfAttention(nn.Module):
    def __init__(self, width: int, heads: int) -> None:
        super().__init__()
        if width % heads:
            raise ValueError("d_model must be divisible by n_heads")
        self.heads = heads
        self.head_width = width // heads
        self.qkv = nn.Linear(width, 3 * width, bias=True)
        self.projection = nn.Linear(width, width, bias=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, length, width = x.shape
        q, k, v = self.qkv(x).view(
            batch, length, 3, self.heads, self.head_width
        ).permute(2, 0, 3, 1, 4).unbind(0)
        output = F.scaled_dot_product_attention(q, k, v, is_causal=True, dropout_p=0.0)
        output = output.transpose(1, 2).contiguous().view(batch, length, width)
        return self.projection(output)


class FeedForward(nn.Module):
    def __init__(self, width: int, expansion: int) -> None:
        super().__init__()
        self.up = nn.Linear(width, expansion, bias=True)
        self.down = nn.Linear(expansion, width, bias=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.down(F.gelu(self.up(x), approximate="tanh"))


class TransformerUpdate(nn.Module):
    """One pre-norm attention/MLP update function shared by all variants."""

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.norm_attention = nn.LayerNorm(config.d_model)
        self.attention = CausalSelfAttention(config.d_model, config.n_heads)
        self.norm_mlp = nn.LayerNorm(config.d_model)
        self.mlp = FeedForward(config.d_model, config.ffn_multiple * config.d_model)

    def attention_update(self, x: torch.Tensor) -> torch.Tensor:
        return self.attention(self.norm_attention(x))

    def mlp_update(self, x: torch.Tensor) -> torch.Tensor:
        return self.mlp(self.norm_mlp(x))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        attention = self.attention_update(x)
        return attention + self.mlp_update(x + attention)


def _parameters_for(module: nn.Module) -> tuple[nn.Parameter, ...]:
    return tuple(module.parameters())


def _add_parameter_gradients(
    destination: list[torch.Tensor | None],
    start: int,
    gradients: Iterable[torch.Tensor | None],
) -> None:
    for offset, gradient in enumerate(gradients):
        if gradient is not None:
            index = start + offset
            destination[index] = gradient if destination[index] is None else destination[index] + gradient


class _MidpointStackFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x: torch.Tensor, stack: "ReversibleStack", *parameters):
        if len(stack.blocks) < 2:
            raise ValueError("midpoint stack requires at least two layers")
        p_previous = x
        p_current = p_previous + stack.step_size * stack.blocks[0](p_previous)
        for index in range(1, len(stack.blocks)):
            p_next = p_previous + (2.0 * stack.step_size) * stack.blocks[index](p_current)
            p_previous, p_current = p_current, p_next
        ctx.stack = stack
        ctx.parameter_count = len(parameters)
        ctx.slices = stack.parameter_slices
        ctx.save_for_backward(p_current, p_previous, *parameters)
        return p_current, p_previous

    @staticmethod
    def backward(ctx, grad_final, grad_penultimate):
        saved = ctx.saved_tensors
        p_next, p_current, *parameters = saved
        stack: ReversibleStack = ctx.stack
        grad_final = torch.zeros_like(p_next) if grad_final is None else grad_final
        grad_penultimate = (
            torch.zeros_like(p_current) if grad_penultimate is None else grad_penultimate
        )
        parameter_grads: list[torch.Tensor | None] = [None] * ctx.parameter_count
        grad_next, grad_current = grad_final, grad_penultimate

        for index in range(len(stack.blocks) - 1, 0, -1):
            block = stack.blocks[index]
            begin, end = ctx.slices[index]
            block_parameters = parameters[begin:end]
            with torch.no_grad():
                p_previous = p_next - (2.0 * stack.step_size) * block(p_current)
            with torch.enable_grad():
                p_input = p_current.detach().requires_grad_(True)
                update = block(p_input)
                gradients = torch.autograd.grad(
                    update,
                    (p_input, *block_parameters),
                    grad_outputs=(2.0 * stack.step_size) * grad_next,
                    allow_unused=True,
                )
            grad_current = grad_current + gradients[0]
            _add_parameter_gradients(parameter_grads, begin, gradients[1:])
            grad_previous = grad_next
            p_next, p_current = p_current, p_previous
            grad_next, grad_current = grad_current, grad_previous

        block = stack.blocks[0]
        begin, end = ctx.slices[0]
        block_parameters = parameters[begin:end]
        with torch.enable_grad():
            p_input = p_current.detach().requires_grad_(True)
            update = block(p_input)
            gradients = torch.autograd.grad(
                update,
                (p_input, *block_parameters),
                grad_outputs=stack.step_size * grad_next,
                allow_unused=True,
            )
        grad_input = grad_next + grad_current + gradients[0]
        _add_parameter_gradients(parameter_grads, begin, gradients[1:])
        return (grad_input, None, *parameter_grads)


class _SymplecticEulerStackFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x: torch.Tensor, stack: "ReversibleStack", *parameters):
        p = x
        q = torch.zeros_like(x)
        for block in stack.blocks:
            q = q + stack.step_size * block.attention_update(p)
            p = p + stack.step_size * block.mlp_update(q)
        ctx.stack = stack
        ctx.parameter_count = len(parameters)
        ctx.slices = stack.parameter_slices
        ctx.save_for_backward(p, q, *parameters)
        return p, q

    @staticmethod
    def backward(ctx, grad_p, grad_q):
        saved = ctx.saved_tensors
        p_current, q_current, *parameters = saved
        stack: ReversibleStack = ctx.stack
        grad_p = torch.zeros_like(p_current) if grad_p is None else grad_p
        grad_q = torch.zeros_like(q_current) if grad_q is None else grad_q
        parameter_grads: list[torch.Tensor | None] = [None] * ctx.parameter_count

        for index in range(len(stack.blocks) - 1, -1, -1):
            block = stack.blocks[index]
            begin, end = ctx.slices[index]
            block_parameters = parameters[begin:end]
            attention_parameters = tuple(block.attention_update.__self__.norm_attention.parameters()) + tuple(block.attention.parameters())
            mlp_parameters = tuple(block.norm_mlp.parameters()) + tuple(block.mlp.parameters())
            split = len(attention_parameters)
            with torch.no_grad():
                p_previous = p_current - stack.step_size * block.mlp_update(q_current)
                q_previous = q_current - stack.step_size * block.attention_update(p_previous)
            with torch.enable_grad():
                q_input = q_current.detach().requires_grad_(True)
                mlp_value = block.mlp_update(q_input)
                mlp_gradients = torch.autograd.grad(
                    mlp_value,
                    (q_input, *mlp_parameters),
                    grad_outputs=stack.step_size * grad_p,
                    allow_unused=True,
                )
                grad_q_total = grad_q + mlp_gradients[0]
                p_input = p_previous.detach().requires_grad_(True)
                attention_value = block.attention_update(p_input)
                attention_gradients = torch.autograd.grad(
                    attention_value,
                    (p_input, *attention_parameters),
                    grad_outputs=stack.step_size * grad_q_total,
                    allow_unused=True,
                )
            grad_p = grad_p + attention_gradients[0]
            grad_q = grad_q_total
            _add_parameter_gradients(parameter_grads, begin, attention_gradients[1:])
            _add_parameter_gradients(parameter_grads, begin + split, mlp_gradients[1:])
            p_current, q_current = p_previous, q_previous

        return (grad_p, None, *parameter_grads)


class ReversibleStack(nn.Module):
    def __init__(self, config: Config, variant: str) -> None:
        super().__init__()
        self.variant = variant
        # Midpoint uses h=0.25; the Hamiltonian symplectic-Euler update uses
        # unit coefficients, matching its a=b=1 construction.
        self.step_size = config.step_size if variant == "midpoint" else 1.0
        self.blocks = nn.ModuleList([TransformerUpdate(config) for _ in range(config.n_layers)])
        self.parameter_slices = []
        cursor = 0
        for block in self.blocks:
            end = cursor + len(_parameters_for(block))
            self.parameter_slices.append((cursor, end))
            cursor = end

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        parameters = tuple(self.parameters())
        if self.variant == "midpoint":
            final, _penultimate = _MidpointStackFunction.apply(x, self, *parameters)
            return final
        if self.variant == "symplectic_euler":
            final, _momentum = _SymplecticEulerStackFunction.apply(x, self, *parameters)
            return final
        raise ValueError(f"unknown reversible variant: {self.variant}")

    def reference_forward(self, x: torch.Tensor) -> torch.Tensor:
        """Differentiable equations used by smoke checks, not by training."""
        if self.variant == "midpoint":
            states = [x]
            states.append(states[0] + self.step_size * self.blocks[0](states[0]))
            for index in range(1, len(self.blocks)):
                states.append(
                    states[-2] + 2.0 * self.step_size * self.blocks[index](states[-1])
                )
            return states[-1]
        p = x
        q = torch.zeros_like(x)
        for block in self.blocks:
            q = q + self.step_size * block.attention_update(p)
            p = p + self.step_size * block.mlp_update(q)
        return p


class LanguageModel(nn.Module):
    def __init__(self, config: Config, variant: str = "baseline") -> None:
        super().__init__()
        if variant not in {"baseline", "midpoint", "symplectic_euler"}:
            raise ValueError(f"unsupported variant: {variant}")
        self.config = config
        self.variant = variant
        self.token_embedding = nn.Embedding(config.vocab_size, config.d_model)
        self.position_embedding = nn.Embedding(config.context_length, config.d_model)
        self.layers = (
            nn.ModuleList([TransformerUpdate(config) for _ in range(config.n_layers)])
            if variant == "baseline"
            else None
        )
        self.reversible_stack = (
            None if variant == "baseline" else ReversibleStack(config, variant)
        )
        self.final_norm = nn.LayerNorm(config.d_model)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)
        self.lm_head.weight = self.token_embedding.weight
        self._initialize()

    def _initialize(self) -> None:
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.normal_(module.weight, mean=0.0, std=0.02)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
            elif isinstance(module, nn.Embedding):
                nn.init.normal_(module.weight, mean=0.0, std=0.02)
            elif isinstance(module, nn.LayerNorm):
                nn.init.ones_(module.weight)
                nn.init.zeros_(module.bias)

    def parameter_count(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def hidden(self, token_ids: torch.Tensor) -> torch.Tensor:
        if token_ids.ndim != 2:
            raise ValueError("token ids must have shape [batch, sequence]")
        _batch, length = token_ids.shape
        if length > self.config.context_length:
            raise ValueError("input sequence exceeds configured context length")
        positions = torch.arange(length, device=token_ids.device)
        x = self.token_embedding(token_ids) + self.position_embedding(positions)[None]
        if self.variant == "baseline":
            for layer in self.layers:
                x = x + layer(x)
        else:
            x = self.reversible_stack(x)
        return self.final_norm(x)

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        return self.lm_head(self.hidden(token_ids))

    def loss(
        self,
        token_ids: torch.Tensor,
        targets: torch.Tensor,
        mask: torch.Tensor | None = None,
        chunk_tokens: int = 1_024,
    ) -> torch.Tensor:
        """Exact next-token CE while bounding temporary vocabulary-logit memory."""
        hidden = self.hidden(token_ids).reshape(-1, self.config.d_model)
        flat_targets = targets.reshape(-1)
        if mask is not None:
            flat_mask = mask.reshape(-1).bool()
            hidden = hidden[flat_mask]
            flat_targets = flat_targets[flat_mask]
        if flat_targets.numel() == 0:
            raise ValueError("loss mask contains no contributing tokens")
        loss_sum = hidden.new_zeros(())
        for start in range(0, flat_targets.numel(), chunk_tokens):
            hidden_chunk = hidden[start : start + chunk_tokens]
            target_chunk = flat_targets[start : start + chunk_tokens]
            if torch.is_grad_enabled() and self.training:
                chunk_loss = checkpoint(
                    _output_chunk_cross_entropy,
                    hidden_chunk,
                    target_chunk,
                    self.lm_head.weight,
                    use_reentrant=False,
                )
            else:
                chunk_loss = _output_chunk_cross_entropy(
                    hidden_chunk, target_chunk, self.lm_head.weight
                )
            loss_sum = loss_sum + chunk_loss
        return loss_sum / flat_targets.numel()


def _output_chunk_cross_entropy(
    hidden: torch.Tensor, targets: torch.Tensor, output_weight: torch.Tensor
) -> torch.Tensor:
    return F.cross_entropy(F.linear(hidden, output_weight), targets, reduction="sum")


@dataclass
class TokenStreams:
    train: torch.Tensor
    validation: torch.Tensor
    tokenizer: object | None = None


def save_token_streams(streams: TokenStreams, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"train": streams.train.cpu(), "validation": streams.validation.cpu()}, path)


def load_token_streams(path: Path) -> TokenStreams:
    payload = torch.load(path, map_location="cpu", weights_only=True)
    return TokenStreams(payload["train"], payload["validation"])


def load_fineweb_tokens(config: Config, train_tokens: int | None = None, validation_tokens: int | None = None) -> TokenStreams:
    """Stream deterministic, disjoint FineWeb-Edu train/validation token buffers."""
    try:
        from datasets import load_dataset
        import tiktoken
    except ImportError as error:
        raise RuntimeError("Install the notebook dependencies: datasets and tiktoken") from error

    train_target = config.train_tokens if train_tokens is None else train_tokens
    validation_target = config.validation_tokens if validation_tokens is None else validation_tokens
    tokenizer = tiktoken.get_encoding(config.tokenizer_name)
    train_buffer, validation_buffer = array.array("I"), array.array("I")
    dataset = load_dataset(
        config.data_name,
        name=config.data_config,
        split="train",
        streaming=True,
    )
    for row in dataset:
        text = row.get("text")
        if not isinstance(text, str) or not text.strip():
            continue
        doc_key = str(row.get("id") or hashlib.sha256(text.encode("utf-8")).hexdigest())
        is_validation = int(hashlib.sha256(doc_key.encode("utf-8")).hexdigest()[:8], 16) % 100 < 2
        buffer = validation_buffer if is_validation else train_buffer
        target = validation_target if is_validation else train_target
        if len(buffer) >= target:
            continue
        encoded = tokenizer.encode(text, allowed_special=set(), disallowed_special=())
        encoded.append(tokenizer.eot_token)
        remaining = target - len(buffer)
        buffer.extend(encoded[:remaining])
        if len(train_buffer) >= train_target and len(validation_buffer) >= validation_target:
            break

    if len(train_buffer) < train_target or len(validation_buffer) < validation_target:
        raise RuntimeError(
            f"dataset stream ended early: train={len(train_buffer):,}/{train_target:,}, "
            f"validation={len(validation_buffer):,}/{validation_target:,}"
        )
    train_array = torch.frombuffer(train_buffer, dtype=torch.int32).clone()
    validation_array = torch.frombuffer(validation_buffer, dtype=torch.int32).clone()
    return TokenStreams(train_array, validation_array, tokenizer)


def seed_everything(seed: int) -> None:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if hasattr(torch.backends, "cuda"):
        torch.backends.cuda.matmul.allow_tf32 = True
    if hasattr(torch.backends, "cudnn"):
        torch.backends.cudnn.allow_tf32 = True


def make_batch(
    stream: torch.Tensor,
    batch_size: int,
    context_length: int,
    device: torch.device,
    valid_tokens: int | None = None,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Sample packed windows, optionally masking a final partial token batch."""
    valid_tokens = batch_size * context_length if valid_tokens is None else valid_tokens
    rows = max(1, math.ceil(valid_tokens / context_length))
    lengths = [min(context_length, valid_tokens - row * context_length) for row in range(rows)]
    upper = len(stream) - context_length - 1
    if upper <= 0:
        raise ValueError("token stream is too short for the configured context")
    starts = torch.randint(0, upper, (rows,))
    offsets = torch.arange(context_length + 1)
    windows = stream[starts[:, None] + offsets[None, :]].long()
    inputs, targets = windows[:, :-1].to(device), windows[:, 1:].to(device)
    mask = torch.arange(context_length)[None, :] < torch.tensor(lengths)[:, None]
    return inputs, targets, mask.to(device)


def masked_cross_entropy(logits: torch.Tensor, targets: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    losses = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1), reduction="none")
    flat_mask = mask.reshape(-1).to(losses.dtype)
    return (losses * flat_mask).sum() / flat_mask.sum().clamp_min(1.0)


@torch.no_grad()
def evaluate(model: LanguageModel, stream: torch.Tensor, device: torch.device, tokens: int = 32_768) -> float:
    was_training = model.training
    model.eval()
    total_tokens = min(tokens, len(stream) - 1)
    total_loss, counted = 0.0, 0
    while counted < total_tokens:
        take = min(model.config.context_length, total_tokens - counted)
        ids = stream[counted : counted + take + 1].long().to(device)
        inputs, targets = ids[:-1].unsqueeze(0), ids[1:].unsqueeze(0)
        mask = torch.ones_like(targets, dtype=torch.bool)
        loss = model.loss(inputs, targets)
        total_loss += loss.item() * take
        counted += take
    if was_training:
        model.train()
    return total_loss / max(counted, 1)


def _device_memory(device: torch.device) -> tuple[float | None, float | None]:
    if device.type != "cuda":
        return None, None
    return (
        torch.cuda.max_memory_allocated(device) / (1024**3),
        torch.cuda.max_memory_reserved(device) / (1024**3),
    )


def _cuda_sync(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.synchronize(device)


def train_run(
    config: Config,
    streams: TokenStreams,
    variant: str,
    batch_size: int,
    device: torch.device,
    output_dir: Path,
    run_name: str,
) -> dict:
    seed_everything(config.seed)
    if device.type == "cuda":
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats(device)
    model = LanguageModel(config, variant).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate, weight_decay=0.0, betas=(0.9, 0.95))
    steps = math.ceil(config.train_tokens / (batch_size * config.context_length))
    warmup = max(1, int(steps * config.warmup_fraction))
    scheduler = torch.optim.lr_scheduler.LambdaLR(
        optimizer,
        lambda step: min((step + 1) / warmup, 0.5 * (1.0 + math.cos(math.pi * max(0, step - warmup) / max(1, steps - warmup)))),
    )
    model.train()
    records: list[dict] = []
    tokens_processed = 0
    started = time.perf_counter()
    for step in range(steps):
        current_tokens = min(batch_size * config.context_length, config.train_tokens - tokens_processed)
        inputs, targets, mask = make_batch(
            streams.train, batch_size, config.context_length, device, current_tokens
        )
        optimizer.zero_grad(set_to_none=True)
        loss_mask = None if current_tokens == batch_size * config.context_length else mask
        loss = model.loss(inputs, targets, loss_mask)
        if not torch.isfinite(loss):
            raise RuntimeError(f"non-finite loss at step {step}")
        loss.backward()
        grad_norm = nn.utils.clip_grad_norm_(model.parameters(), config.grad_clip)
        optimizer.step()
        scheduler.step()
        tokens_processed += current_tokens
        if step == 0 or (step + 1) % config.eval_interval == 0 or step + 1 == steps:
            record = {
                "step": step + 1,
                "training_tokens": tokens_processed,
                "loss": float(loss.detach().item()),
                "learning_rate": float(scheduler.get_last_lr()[0]),
                "gradient_norm": float(grad_norm.detach().item()),
            }
            records.append(record)
            print(
                f"[{run_name}] step {step + 1:,}/{steps:,} | "
                f"tokens {tokens_processed:,}/{config.train_tokens:,} | loss {record['loss']:.4f}",
                flush=True,
            )
    _cuda_sync(device)
    elapsed = time.perf_counter() - started
    final_validation_loss = evaluate(model, streams.validation, device)
    allocated, reserved = _device_memory(device)
    run_record = {
        "run_name": run_name,
        "variant": variant,
        "step_size": model.reversible_stack.step_size if model.reversible_stack is not None else None,
        "batch_sequences": batch_size,
        "context_length": config.context_length,
        "batch_tokens": batch_size * config.context_length,
        "training_tokens": tokens_processed,
        "steps": steps,
        "elapsed_training_seconds": elapsed,
        "training_tokens_per_second": tokens_processed / max(elapsed, 1e-9),
        "final_training_loss": records[-1]["loss"],
        "final_validation_loss": final_validation_loss,
        "peak_gpu_allocated_gib": allocated,
        "peak_gpu_reserved_gib": reserved,
        "device": str(device),
        "parameter_count": model.parameter_count(),
        "output_loss_chunk_tokens": 1_024,
        "weight_decay": 0.0,
        "dropout": 0.0,
        "seed": config.seed,
        "curve": records,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{run_name}.json").write_text(json.dumps(run_record, indent=2))
    with (output_dir / f"{run_name}_loss.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    del optimizer, scheduler, model, inputs, targets, mask, loss
    gc.collect()
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return run_record


def _one_step_probe(
    config: Config, streams: TokenStreams, variant: str, batch_size: int, device: torch.device
) -> tuple[bool, float | None, float | None]:
    try:
        seed_everything(config.seed)
        if device.type == "cuda":
            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats(device)
        model = LanguageModel(config, variant).to(device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate, weight_decay=0.0)
        inputs, targets, mask = make_batch(streams.train, batch_size, config.context_length, device)
        optimizer.zero_grad(set_to_none=True)
        loss = model.loss(inputs, targets)
        loss.backward()
        optimizer.step()
        _cuda_sync(device)
        peak_allocated = torch.cuda.max_memory_allocated(device) / (1024**3) if device.type == "cuda" else None
        peak_reserved = torch.cuda.max_memory_reserved(device) / (1024**3) if device.type == "cuda" else None
        del optimizer, model, inputs, targets, mask, loss
        gc.collect()
        if device.type == "cuda":
            torch.cuda.empty_cache()
        return True, peak_allocated, peak_reserved
    except (RuntimeError, torch.cuda.OutOfMemoryError) as error:
        if "out of memory" not in str(error).lower() and not isinstance(error, torch.cuda.OutOfMemoryError):
            raise
        gc.collect()
        if device.type == "cuda":
            torch.cuda.empty_cache()
        return False, None, None


def calibrate_max_batch(
    config: Config,
    streams: TokenStreams,
    variant: str,
    device: torch.device,
    max_batch: int = 1024,
    memory_fraction: float = 0.70,
) -> tuple[int, list[dict]]:
    """Find the largest tested sequence batch with a safe memory headroom."""
    if device.type != "cuda":
        raise RuntimeError("Colab full-run batch calibration requires a CUDA GPU")
    total_memory = torch.cuda.get_device_properties(device).total_memory / (1024**3)
    successful: list[int] = []
    probes: list[dict] = []
    candidate = 1
    while candidate <= max_batch:
        okay, peak_allocated, peak_reserved = _one_step_probe(config, streams, variant, candidate, device)
        safe = okay and peak_reserved is not None and peak_reserved <= total_memory * memory_fraction
        probes.append({"batch_sequences": candidate, "completed": okay, "peak_allocated_gib": peak_allocated, "peak_reserved_gib": peak_reserved, "safe": safe})
        if not safe:
            break
        successful.append(candidate)
        candidate *= 2
    if not successful:
        raise RuntimeError(f"No safe batch size fits for {variant} on {device}")
    lower = successful[-1]
    upper = min(candidate - 1, max_batch)
    while lower < upper:
        middle = (lower + upper + 1) // 2
        okay, peak_allocated, peak_reserved = _one_step_probe(config, streams, variant, middle, device)
        safe = okay and peak_reserved is not None and peak_reserved <= total_memory * memory_fraction
        probes.append({"batch_sequences": middle, "completed": okay, "peak_allocated_gib": peak_allocated, "peak_reserved_gib": peak_reserved, "safe": safe})
        if safe:
            lower = middle
        else:
            upper = middle - 1
    return lower, probes


def _reference_gradients(stack: ReversibleStack, x: torch.Tensor) -> tuple[torch.Tensor, list[torch.Tensor]]:
    output = stack.reference_forward(x)
    loss = output.square().mean()
    gradients = torch.autograd.grad(loss, (x, *stack.parameters()))
    return loss.detach(), [gradient.detach() for gradient in gradients]


def run_smoke_checks() -> dict:
    """CPU design checks for parameter count, causality, inversion and gradients."""
    torch.set_num_threads(1)
    config = Config(vocab_size=64, context_length=16, d_model=32, n_heads=4, n_layers=3, train_tokens=256)
    results: dict[str, object] = {"device": "cpu", "checks": {}}
    full_config = Config()
    full_model = LanguageModel(full_config, "baseline")
    parameter_count = full_model.parameter_count()
    assert 19_000_000 <= parameter_count <= 21_000_000, parameter_count
    results["parameter_count"] = parameter_count
    del full_model

    torch.manual_seed(2026)
    lm = LanguageModel(config, "baseline")
    ids = torch.randint(0, config.vocab_size, (2, config.context_length))
    logits = lm(ids)
    loss = F.cross_entropy(logits[:, :-1].reshape(-1, config.vocab_size), ids[:, 1:].reshape(-1))
    loss.backward()
    assert torch.isfinite(loss) and all(p.grad is None or torch.isfinite(p.grad).all() for p in lm.parameters())
    results["checks"]["causal_loss_backward"] = float(loss.detach())
    comparison_model = LanguageModel(config, "baseline")
    comparison_input, comparison_targets = ids[:, :-1], ids[:, 1:]
    comparison_mask = torch.ones_like(comparison_targets, dtype=torch.bool)
    full_loss = F.cross_entropy(
        comparison_model(comparison_input).reshape(-1, config.vocab_size),
        comparison_targets.reshape(-1),
    )
    full_gradients = torch.autograd.grad(full_loss, tuple(comparison_model.parameters()))
    chunk_loss = comparison_model.loss(
        comparison_input, comparison_targets, comparison_mask, chunk_tokens=7
    )
    chunk_gradients = torch.autograd.grad(chunk_loss, tuple(comparison_model.parameters()))
    chunk_gradient_error = max(
        (full_gradient - chunk_gradient).abs().max().item()
        for full_gradient, chunk_gradient in zip(full_gradients, chunk_gradients)
    )
    assert torch.allclose(full_loss, chunk_loss, atol=2e-6, rtol=2e-6)
    assert chunk_gradient_error < 2e-5, chunk_gradient_error
    results["checks"]["chunked_loss_max_gradient_error"] = chunk_gradient_error
    with torch.no_grad():
        changed = ids.clone()
        changed[:, 10:] = torch.randint(0, config.vocab_size, changed[:, 10:].shape)
        before = lm(ids)
        after = lm(changed)
    assert torch.allclose(before[:, :10], after[:, :10], atol=1e-6, rtol=1e-6)
    results["checks"]["causal_mask"] = "passed"
    del lm

    batch_inputs, batch_targets, batch_mask = make_batch(
        torch.randint(0, config.vocab_size, (4_096,), dtype=torch.int32),
        2,
        config.context_length,
        torch.device("cpu"),
        valid_tokens=77,
    )
    assert int(batch_mask.sum()) == 77
    assert torch.equal(batch_inputs[:, 1:][batch_mask[:, 1:]], batch_targets[:, :-1][batch_mask[:, 1:]])
    results["checks"]["next_token_shift_and_exact_partial_batch"] = "passed"

    for variant in ("midpoint", "symplectic_euler"):
        torch.manual_seed(42)
        stack = ReversibleStack(config, variant)
        with torch.no_grad():
            initial_state = torch.randn(2, config.context_length, config.d_model)
            if variant == "midpoint":
                states = [initial_state]
                states.append(states[0] + stack.step_size * stack.blocks[0](states[0]))
                for index in range(1, len(stack.blocks)):
                    states.append(states[-2] + 2.0 * stack.step_size * stack.blocks[index](states[-1]))
                p_next, p_current = states[-1], states[-2]
                reconstruction_errors = []
                for index in range(len(stack.blocks) - 1, 0, -1):
                    p_previous = p_next - 2.0 * stack.step_size * stack.blocks[index](p_current)
                    reconstruction_errors.append((p_previous - states[index - 1]).abs().max().item())
                    p_next, p_current = p_current, p_previous
            else:
                p_states = [initial_state]
                q_states = [torch.zeros_like(initial_state)]
                for block in stack.blocks:
                    q_next = q_states[-1] + stack.step_size * block.attention_update(p_states[-1])
                    p_next = p_states[-1] + stack.step_size * block.mlp_update(q_next)
                    q_states.append(q_next)
                    p_states.append(p_next)
                p_current, q_current = p_states[-1], q_states[-1]
                reconstruction_errors = []
                for index in range(len(stack.blocks) - 1, -1, -1):
                    p_previous = p_current - stack.step_size * stack.blocks[index].mlp_update(q_current)
                    q_previous = q_current - stack.step_size * stack.blocks[index].attention_update(p_previous)
                    reconstruction_errors.extend(
                        ((p_previous - p_states[index]).abs().max().item(),
                         (q_previous - q_states[index]).abs().max().item())
                    )
                    p_current, q_current = p_previous, q_previous
        max_reconstruction_error = max(reconstruction_errors)
        assert max_reconstruction_error < 2e-5, (variant, max_reconstruction_error)
        x_reversible = torch.randn(2, config.context_length, config.d_model, requires_grad=True)
        x_reference = x_reversible.detach().clone().requires_grad_(True)
        custom_loss = stack(x_reversible).square().mean()
        custom_gradients = torch.autograd.grad(custom_loss, (x_reversible, *stack.parameters()))
        reference_loss, reference_gradients = _reference_gradients(stack, x_reference)
        assert torch.allclose(custom_loss, reference_loss, atol=2e-6, rtol=2e-6), variant
        max_gradient_error = max(
            (left.detach() - right).abs().max().item()
            for left, right in zip(custom_gradients, reference_gradients)
        )
        assert max_gradient_error < 2e-4, (variant, max_gradient_error)
        results["checks"][variant] = {
            "loss": float(custom_loss.detach()),
            "max_gradient_absolute_error": max_gradient_error,
            "max_reconstruction_absolute_error": max_reconstruction_error,
        }
        del stack, x_reversible, x_reference

    tiny_stream = torch.randint(0, config.vocab_size, (4_096,), dtype=torch.int32)
    x, y, mask = make_batch(tiny_stream, 2, config.context_length, torch.device("cpu"))
    for variant in ("baseline", "midpoint", "symplectic_euler"):
        tiny_model = LanguageModel(config, variant)
        tiny_optimizer = torch.optim.AdamW(tiny_model.parameters(), lr=1e-3, weight_decay=0.0)
        tiny_optimizer.zero_grad(set_to_none=True)
        tiny_loss = tiny_model.loss(x, y, mask, chunk_tokens=7)
        tiny_loss.backward()
        tiny_optimizer.step()
        assert torch.isfinite(tiny_loss)
        results["checks"][f"optimizer_step_{variant}"] = "passed"
        del tiny_optimizer, tiny_model, tiny_loss
    results["status"] = "passed"
    return results


def run_experiment(
    config: Config,
    streams: TokenStreams,
    device: torch.device,
    output_dir: Path,
    fixed_batch_size: int | None = None,
    maximum_batch_size: int = 1024,
) -> dict:
    if device.type != "cuda":
        raise RuntimeError("The 50M-token experiment is intended for a Colab CUDA GPU")
    baseline_batch, baseline_probes = calibrate_max_batch(config, streams, "baseline", device, maximum_batch_size)
    fixed_batch = baseline_batch if fixed_batch_size is None else fixed_batch_size
    if fixed_batch > baseline_batch:
        raise ValueError("fixed batch size exceeds the calibrated baseline maximum")
    results: list[dict] = []
    results.append(train_run(config, streams, "baseline", fixed_batch, device, output_dir, "baseline_fixed"))
    midpoint = train_run(config, streams, "midpoint", fixed_batch, device, output_dir, "midpoint_fixed")
    symplectic = train_run(config, streams, "symplectic_euler", fixed_batch, device, output_dir, "symplectic_euler_fixed")
    results.extend((midpoint, symplectic))
    winner = min((midpoint, symplectic), key=lambda result: result["final_validation_loss"])
    max_batch, reversible_probes = calibrate_max_batch(
        config, streams, winner["variant"], device, maximum_batch_size
    )
    maximum_run = train_run(
        config,
        streams,
        winner["variant"],
        max_batch,
        device,
        output_dir,
        f"{winner['variant']}_maximum_batch",
    )
    results.append(maximum_run)
    experiment = {
        "config": config.as_dict(),
        "device_name": torch.cuda.get_device_name(device),
        "device_total_memory_gib": torch.cuda.get_device_properties(device).total_memory / (1024**3),
        "fixed_batch_sequences": fixed_batch,
        "fixed_batch_tokens": fixed_batch * config.context_length,
        "baseline_batch_probes": baseline_probes,
        "selected_reversible_variant": winner["variant"],
        "maximum_reversible_batch_sequences": max_batch,
        "maximum_reversible_batch_tokens": max_batch * config.context_length,
        "maximum_reversible_batch_search_cap": maximum_batch_size,
        "maximum_reversible_batch_cap_reached": max_batch == maximum_batch_size,
        "reversible_batch_probes": reversible_probes,
        "runs": results,
    }
    (output_dir / "session13_results.json").write_text(json.dumps(experiment, indent=2))
    write_report(experiment, output_dir)
    return experiment


def write_report(experiment: dict, output_dir: Path) -> None:
    """Create a compact Markdown result table and loss-curve figure."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        plt = None
    rows = [
        "# Session 13 training results",
        "",
        f"- GPU: {experiment['device_name']} ({experiment['device_total_memory_gib']:.1f} GiB)",
        f"- Model parameters: {experiment['config']['parameter_count']:,}",
        f"- Training tokens per run: {experiment['config']['train_tokens']:,}",
        f"- Fixed batch: {experiment['fixed_batch_sequences']} sequences × {experiment['config']['context_length']} tokens",
        f"- Reversible variant selected by lowest fixed-batch validation loss: {experiment['selected_reversible_variant']}",
        f"- Maximum tested reversible batch: {experiment['maximum_reversible_batch_sequences']} sequences × {experiment['config']['context_length']} tokens",
        f"- Maximum-batch search cap reached: {experiment['maximum_reversible_batch_cap_reached']} (cap {experiment['maximum_reversible_batch_search_cap']} sequences)",
        "",
        "| Run | Variant | Batch tokens | Final train loss | Final validation loss | Tokens/s | Peak allocated GiB | Peak reserved GiB |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for run in experiment["runs"]:
        allocated = "n/a" if run["peak_gpu_allocated_gib"] is None else f"{run['peak_gpu_allocated_gib']:.2f}"
        reserved = "n/a" if run["peak_gpu_reserved_gib"] is None else f"{run['peak_gpu_reserved_gib']:.2f}"
        rows.append(
            f"| {run['run_name']} | {run['variant']} | {run['batch_tokens']:,} | "
            f"{run['final_training_loss']:.4f} | {run['final_validation_loss']:.4f} | "
            f"{run['training_tokens_per_second']:.1f} | {allocated} | {reserved} |"
        )
    rows += [
        "",
        "All fixed-batch runs use the same data split, seed, context, optimizer settings, and exact token budget. "
        "Weight decay and dropout are zero for every run. Peak GPU figures are measured by PyTorch and do not include other processes using the device.",
        "",
        "Cost is not estimated because Colab pricing and free-tier availability vary. Record the runtime tier and any billed amount from the account used for the run if cost comparison is required.",
        "",
        "Loss curves are saved as per-run CSV files. See `session13_results.json` for configuration and batch calibration details.",
    ]
    (output_dir / "REPORT.md").write_text("\n".join(rows) + "\n")
    if plt is not None:
        figure, axis = plt.subplots(figsize=(9, 5))
        for run in experiment["runs"]:
            curve = run["curve"]
            axis.plot(
                [point["training_tokens"] / 1_000_000 for point in curve],
                [point["loss"] for point in curve],
                label=run["run_name"],
            )
        axis.set(xlabel="Training tokens (millions)", ylabel="Training cross-entropy", title="Session 13 loss curves")
        axis.grid(alpha=0.25)
        axis.legend(fontsize=8)
        figure.tight_layout()
        figure.savefig(output_dir / "loss_curves.png", dpi=160)
        plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true", help="run tiny CPU architecture and gradient checks")
    parser.add_argument("--print-parameter-count", action="store_true")
    args = parser.parse_args()
    if args.smoke:
        print(json.dumps(run_smoke_checks(), indent=2))
    elif args.print_parameter_count:
        print(LanguageModel(Config(), "baseline").parameter_count())
    else:
        parser.error("use --smoke for local checks or run the Colab notebook for full training")


if __name__ == "__main__":
    main()
