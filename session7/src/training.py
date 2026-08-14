from __future__ import annotations

from dataclasses import dataclass
import math
import time

import torch
from torch import nn

from .config import ExperimentConfig
from .data import BalancedBatcher, DataBundle
from .decoders import TokenByteCodec, parameter_count
from .transformer import ReverseKroneckerLM


@dataclass
class TrainResult:
    model: ReverseKroneckerLM
    record: dict


def set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    try:
        torch.use_deterministic_algorithms(True)
    except RuntimeError:
        pass


def _lr_factor(step: int, total_steps: int, warmup_fraction: float) -> float:
    warmup = max(1, int(total_steps * warmup_fraction))
    if step < warmup:
        return (step + 1) / warmup
    progress = (step - warmup) / max(1, total_steps - warmup)
    return 0.5 * (1.0 + math.cos(math.pi * progress))


def train_language_model(
    data: DataBundle,
    codec: TokenByteCodec,
    config: ExperimentConfig,
    head_name: str,
    seed: int,
    learning_rate: float,
    backbone_state: dict[str, torch.Tensor],
    steps: int | None = None,
) -> TrainResult:
    set_seed(seed + {"vocabulary": 0, "parallel_byte": 101, "autoregressive_byte": 202}[head_name])
    model = ReverseKroneckerLM(data.vocab, config, head_name, backbone_state)
    model.train()
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=learning_rate, weight_decay=config.weight_decay
    )
    total_steps = steps or config.steps
    scheduler = torch.optim.lr_scheduler.LambdaLR(
        optimizer,
        lambda step: _lr_factor(step, total_steps, config.warmup_fraction),
    )
    batcher = BalancedBatcher(
        data.token_ids["train"], config.batch_size, config.context_length, seed
    )
    curve: list[dict] = []
    peak_logits_bytes = 0
    started = time.perf_counter()
    log_every = max(1, total_steps // 20)

    for step in range(total_steps):
        input_ids, target_ids, _ = batcher.next()
        optimizer.zero_grad(set_to_none=True)
        output = model.loss(input_ids, target_ids, codec)
        if not torch.isfinite(output.loss):
            raise RuntimeError(f"non-finite loss at step {step}: {output.loss.item()}")
        output.loss.backward()
        gradient_norm = nn.utils.clip_grad_norm_(model.parameters(), config.grad_clip)
        optimizer.step()
        scheduler.step()
        peak_logits_bytes = max(peak_logits_bytes, output.peak_logits_bytes)
        if step == 0 or (step + 1) % log_every == 0 or step + 1 == total_steps:
            curve.append(
                {
                    "step": step + 1,
                    "tokens": (step + 1) * config.batch_size * config.context_length,
                    "loss": float(output.loss.detach().item()),
                    "learning_rate": float(scheduler.get_last_lr()[0]),
                    "gradient_norm": float(gradient_norm),
                }
            )

    elapsed = time.perf_counter() - started
    record = {
        "architecture": head_name,
        "seed": seed,
        "learning_rate": learning_rate,
        "steps": total_steps,
        "training_tokens": total_steps * config.batch_size * config.context_length,
        "elapsed_seconds": elapsed,
        "training_tokens_per_second": (
            total_steps * config.batch_size * config.context_length / max(elapsed, 1e-9)
        ),
        "head_parameters": parameter_count(model.head),
        "backbone_parameters": parameter_count(model.backbone),
        "total_parameters": parameter_count(model),
        "peak_training_logits_bytes": peak_logits_bytes,
        "curve": curve,
    }
    return TrainResult(model, record)

