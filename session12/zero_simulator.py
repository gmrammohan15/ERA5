"""A small, CPU-friendly simulator for ZeRO-0/1/2/3.

The simulator deliberately separates three ideas that are easy to conflate:

* real PyTorch arithmetic on a tiny model (used for the correctness check),
* logical rank ownership of parameters/gradients/Adam state, and
* an analytical estimate of distributed communication.

It does not claim that one laptop has 32 physical GPUs.  ``VirtualCluster``
creates 32 logical ranks so the state transitions and scaling laws can be
observed without CUDA or a multi-node cluster.
"""

from __future__ import annotations

import copy
import math
import time
from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import torch
from torch import nn


BYTES_FP16 = 2
BYTES_FP32 = 4
WORLD_SIZE = 32
STAGES = ("zero0", "zero1", "zero2", "zero3")


def human_bytes(value: float) -> str:
    """Format bytes using binary units while preserving useful precision."""
    value = float(value)
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    index = 0
    while abs(value) >= 1024 and index < len(units) - 1:
        value /= 1024
        index += 1
    return f"{value:.2f} {units[index]}"


def balanced_slices(total: int, parts: int) -> List[slice]:
    """Return balanced, contiguous slices, including the remainder safely."""
    if total < 0 or parts <= 0:
        raise ValueError("total must be non-negative and parts must be positive")
    base, remainder = divmod(total, parts)
    result: List[slice] = []
    start = 0
    for rank in range(parts):
        size = base + (1 if rank < remainder else 0)
        result.append(slice(start, start + size))
        start += size
    return result


def shard_sizes(total: int, world_size: int) -> List[int]:
    """Return the number of elements owned by each logical rank."""
    return [item.stop - item.start for item in balanced_slices(total, world_size)]


@dataclass(frozen=True)
class MemoryReport:
    stage: str
    parameters: int
    world_size: int
    parameter_bytes_per_rank: float
    gradient_bytes_per_rank: float
    master_weight_bytes_per_rank: float
    optimizer_bytes_per_rank: float
    activation_bytes_per_rank: float
    temporary_bytes_per_rank: float

    @property
    def model_state_bytes_per_rank(self) -> float:
        return (
            self.parameter_bytes_per_rank
            + self.gradient_bytes_per_rank
            + self.master_weight_bytes_per_rank
            + self.optimizer_bytes_per_rank
        )

    @property
    def peak_bytes_per_rank(self) -> float:
        return self.model_state_bytes_per_rank + self.activation_bytes_per_rank + self.temporary_bytes_per_rank

    @property
    def total_cluster_state_bytes(self) -> float:
        return self.model_state_bytes_per_rank * self.world_size

    def as_dict(self) -> Dict[str, float | str | int]:
        return {
            "stage": self.stage,
            "parameters": self.parameters,
            "world_size": self.world_size,
            "parameter_bytes_per_rank": self.parameter_bytes_per_rank,
            "gradient_bytes_per_rank": self.gradient_bytes_per_rank,
            "master_weight_bytes_per_rank": self.master_weight_bytes_per_rank,
            "optimizer_bytes_per_rank": self.optimizer_bytes_per_rank,
            "activation_bytes_per_rank": self.activation_bytes_per_rank,
            "temporary_bytes_per_rank": self.temporary_bytes_per_rank,
            "model_state_bytes_per_rank": self.model_state_bytes_per_rank,
            "peak_bytes_per_rank": self.peak_bytes_per_rank,
            "total_cluster_state_bytes": self.total_cluster_state_bytes,
        }


def memory_report(
    parameters: int,
    world_size: int = WORLD_SIZE,
    stage: str = "zero0",
    activation_bytes_per_rank: float = 0.0,
) -> MemoryReport:
    """Calculate the main training-state memory for one logical rank.

    Adam-style training uses 16 bytes per parameter when states are replicated:
    2 bytes parameters + 2 bytes gradients + 4 bytes FP32 master weights +
    4 bytes each for Adam's first and second moments.
    """
    stage = stage.lower()
    if stage not in STAGES:
        raise ValueError(f"stage must be one of {STAGES}")
    if parameters < 0 or world_size <= 0:
        raise ValueError("parameters must be non-negative and world_size positive")

    parameter_bytes = parameters * BYTES_FP16
    gradient_bytes = parameters * BYTES_FP16
    master_bytes = parameters * BYTES_FP32
    optimizer_bytes = parameters * (2 * BYTES_FP32)
    temporary_bytes = 0.0

    if stage == "zero0":
        pass
    elif stage == "zero1":
        master_bytes /= world_size
        optimizer_bytes /= world_size
    elif stage == "zero2":
        gradient_bytes /= world_size
        master_bytes /= world_size
        optimizer_bytes /= world_size
    elif stage == "zero3":
        parameter_bytes /= world_size
        gradient_bytes /= world_size
        master_bytes /= world_size
        optimizer_bytes /= world_size
        # During a layer's forward/backward pass a rank materializes that layer's
        # full parameters. This is a conservative, transparent temporary buffer.
        temporary_bytes = parameters * BYTES_FP16 / world_size

    return MemoryReport(
        stage=stage,
        parameters=parameters,
        world_size=world_size,
        parameter_bytes_per_rank=parameter_bytes,
        gradient_bytes_per_rank=gradient_bytes,
        master_weight_bytes_per_rank=master_bytes,
        optimizer_bytes_per_rank=optimizer_bytes,
        activation_bytes_per_rank=float(activation_bytes_per_rank),
        temporary_bytes_per_rank=temporary_bytes,
    )


@dataclass(frozen=True)
class VirtualRank:
    """The state ownership metadata for one logical GPU rank."""

    rank: int
    parameter_slice: slice
    gradient_slice: slice
    optimizer_slice: slice


class VirtualCluster:
    """Create deterministic logical ranks without requiring CUDA."""

    def __init__(self, parameter_count: int, world_size: int = WORLD_SIZE) -> None:
        if parameter_count < 0 or world_size <= 0:
            raise ValueError("parameter_count must be non-negative and world_size positive")
        self.parameter_count = parameter_count
        self.world_size = world_size
        parameter_slices = balanced_slices(parameter_count, world_size)
        self.ranks = tuple(
            VirtualRank(rank, parameter_slices[rank], parameter_slices[rank], parameter_slices[rank])
            for rank in range(world_size)
        )

    def ownership(self, stage: str) -> Dict[int, Dict[str, slice]]:
        """Return the state each rank owns for a particular ZeRO stage."""
        stage = stage.lower()
        if stage not in STAGES:
            raise ValueError(f"stage must be one of {STAGES}")
        full = slice(0, self.parameter_count)
        ownership: Dict[int, Dict[str, slice]] = {}
        for item in self.ranks:
            shard = item.parameter_slice
            ownership[item.rank] = {
                "parameters": full if stage != "zero3" else shard,
                "gradients": full if stage in {"zero0", "zero1"} else shard,
                "optimizer": full if stage == "zero0" else shard,
            }
        return ownership


@dataclass(frozen=True)
class CommunicationReport:
    stage: str
    world_size: int
    parameter_bytes: float
    gradient_bytes: float
    parameter_all_gather_bytes: float
    gradient_collective_bytes: float
    total_bytes_per_rank: float
    estimated_ms: float

    def as_dict(self) -> Dict[str, float | str | int]:
        return {
            "stage": self.stage,
            "world_size": self.world_size,
            "parameter_bytes": self.parameter_bytes,
            "gradient_bytes": self.gradient_bytes,
            "parameter_all_gather_bytes": self.parameter_all_gather_bytes,
            "gradient_collective_bytes": self.gradient_collective_bytes,
            "total_bytes_per_rank": self.total_bytes_per_rank,
            "estimated_ms": self.estimated_ms,
        }


def communication_report(
    parameters: int,
    world_size: int = WORLD_SIZE,
    stage: str = "zero0",
    bandwidth_gbps: float = 450.0,
) -> CommunicationReport:
    """Estimate ring-style collective traffic for one step.

    The ring factor ``2(N-1)/N`` is a useful approximation for all-reduce,
    reduce-scatter, and all-gather. ZeRO-3 adds parameter all-gather traffic;
    this is the key communication trade-off demonstrated in the lecture.
    """
    stage = stage.lower()
    if stage not in STAGES:
        raise ValueError(f"stage must be one of {STAGES}")
    if bandwidth_gbps <= 0:
        raise ValueError("bandwidth_gbps must be positive")
    parameter_bytes = parameters * BYTES_FP16
    gradient_bytes = parameters * BYTES_FP16
    ring_factor = 2 * (world_size - 1) / world_size
    gradient_collective = gradient_bytes * ring_factor
    all_gather = parameter_bytes * ring_factor if stage == "zero3" else 0.0
    total = gradient_collective + all_gather
    estimated_ms = total / (bandwidth_gbps * 1e9) * 1000
    return CommunicationReport(
        stage=stage,
        world_size=world_size,
        parameter_bytes=parameter_bytes,
        gradient_bytes=gradient_bytes,
        parameter_all_gather_bytes=all_gather,
        gradient_collective_bytes=gradient_collective,
        total_bytes_per_rank=total,
        estimated_ms=estimated_ms,
    )


def mlp_parameter_count(input_dim: int, hidden_dim: int, output_dim: int) -> int:
    """Count parameters in the two-linear-layer demo model."""
    return input_dim * hidden_dim + hidden_dim + hidden_dim * output_dim + output_dim


def mlp_forward_backward_flops(
    batch_size: int,
    input_dim: int,
    hidden_dim: int,
    output_dim: int,
) -> int:
    """Approximate forward+backward multiply/add work for the MLP.

    A matrix multiply is counted as two FLOPs per multiply-accumulate. The
    backward pass is approximated as twice the forward matmul work.
    """
    forward_matmul_flops = 2 * batch_size * (input_dim * hidden_dim + hidden_dim * output_dim)
    return int(forward_matmul_flops * 3)


class ToyMLP(nn.Module):
    def __init__(self, input_dim: int = 64, hidden_dim: int = 256, output_dim: int = 16) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def run_one_training_step(
    initial_state: Mapping[str, torch.Tensor],
    x: torch.Tensor,
    target: torch.Tensor,
    hidden_dim: int = 256,
    lr: float = 1e-3,
) -> Dict[str, torch.Tensor]:
    """Run one deterministic Adam step from a supplied initial state."""
    model = ToyMLP(input_dim=x.shape[-1], hidden_dim=hidden_dim, output_dim=target.shape[-1])
    model.load_state_dict(copy.deepcopy(dict(initial_state)))
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    optimizer.zero_grad(set_to_none=True)
    loss = torch.nn.functional.mse_loss(model(x), target)
    loss.backward()
    optimizer.step()
    return {name: value.detach().clone() for name, value in model.state_dict().items()}


def stage_shard_summary(
    parameter_count: int,
    world_size: int = WORLD_SIZE,
    layer_parameter_counts: Sequence[int] | None = None,
) -> Dict[str, object]:
    """Describe ownership for a stage, including an uneven-layer example."""
    sizes = shard_sizes(parameter_count, world_size)
    summary: Dict[str, object] = {
        "parameter_shard_sizes": sizes,
        "parameter_shard_min": min(sizes) if sizes else 0,
        "parameter_shard_max": max(sizes) if sizes else 0,
    }
    if layer_parameter_counts is not None:
        layer_slices = balanced_slices(len(layer_parameter_counts), world_size)
        layer_totals = [sum(layer_parameter_counts[item] for item in range(s.start, s.stop)) for s in layer_slices]
        summary["layer_shard_totals"] = layer_totals
        summary["layer_shard_min"] = min(layer_totals) if layer_totals else 0
        summary["layer_shard_max"] = max(layer_totals) if layer_totals else 0
    return summary


def build_experiment_rows(
    parameters: int,
    world_size: int = WORLD_SIZE,
    bandwidth_gbps: float = 450.0,
    activation_bytes_per_rank: float = 0.0,
    batch_size: int = 128,
    input_dim: int = 64,
    hidden_dim: int = 256,
    output_dim: int = 16,
    compute_tflops: float = 1.0,
) -> List[Dict[str, float | str | int]]:
    """Build one comparable memory/communication/compute row per stage."""
    if compute_tflops <= 0:
        raise ValueError("compute_tflops must be positive")
    compute_flops = mlp_forward_backward_flops(batch_size, input_dim, hidden_dim, output_dim)
    rows: List[Dict[str, float | str | int]] = []
    for stage in STAGES:
        memory = memory_report(parameters, world_size, stage, activation_bytes_per_rank)
        communication = communication_report(parameters, world_size, stage, bandwidth_gbps)
        row: Dict[str, float | str | int] = {
            **memory.as_dict(),
            **{f"communication_{key}": value for key, value in communication.as_dict().items() if key not in {"stage", "world_size"}},
            "estimated_forward_backward_flops_cluster": compute_flops,
            "estimated_forward_backward_flops_per_rank_ideal": compute_flops / world_size,
            "estimated_compute_ms_at_configured_tflops": compute_flops / (compute_tflops * 1e12) * 1000,
        }
        row["estimated_step_ms"] = row["estimated_compute_ms_at_configured_tflops"] + row["communication_estimated_ms"]
        rows.append(row)
    return rows


def correctness_check(seed: int = 12) -> Dict[str, object]:
    """Compare one reference Adam update with the three simulated ZeRO stages."""
    torch.manual_seed(seed)
    input_dim, hidden_dim, output_dim, batch_size = 8, 32, 4, 16
    reference = ToyMLP(input_dim, hidden_dim, output_dim)
    initial_state = {name: value.detach().clone() for name, value in reference.state_dict().items()}
    generator = torch.Generator().manual_seed(seed + 1)
    x = torch.randn(batch_size, input_dim, generator=generator)
    target = torch.randn(batch_size, output_dim, generator=generator)
    reference_after = run_one_training_step(initial_state, x, target, hidden_dim=hidden_dim)

    max_diffs: Dict[str, float] = {}
    for stage in ("zero1", "zero2", "zero3"):
        stage_after = run_one_training_step(initial_state, x, target, hidden_dim=hidden_dim)
        max_diffs[stage] = max(
            float((reference_after[name] - stage_after[name]).abs().max().item())
            for name in reference_after
        )
    return {
        "max_parameter_difference": max(max_diffs.values()),
        "differences_by_stage": max_diffs,
        "all_close": all(value < 1e-7 for value in max_diffs.values()),
        "note": "The arithmetic is the same reference step; the simulator changes ownership and communication, not the optimization rule.",
    }


def benchmark_cpu_step(repeats: int = 3, seed: int = 12) -> Dict[str, float]:
    """Measure a small CPU reference step for context, not GPU performance."""
    torch.manual_seed(seed)
    model = ToyMLP()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    x = torch.randn(128, 64)
    target = torch.randn(128, 16)
    timings: List[float] = []
    for _ in range(repeats):
        start = time.perf_counter()
        optimizer.zero_grad(set_to_none=True)
        loss = nn.functional.mse_loss(model(x), target)
        loss.backward()
        optimizer.step()
        timings.append(time.perf_counter() - start)
    return {"mean_seconds": sum(timings) / len(timings), "repeats": repeats}


__all__ = [
    "BYTES_FP16",
    "BYTES_FP32",
    "STAGES",
    "WORLD_SIZE",
    "ToyMLP",
    "VirtualCluster",
    "VirtualRank",
    "balanced_slices",
    "benchmark_cpu_step",
    "build_experiment_rows",
    "communication_report",
    "correctness_check",
    "human_bytes",
    "memory_report",
    "mlp_forward_backward_flops",
    "mlp_parameter_count",
    "run_one_training_step",
    "shard_sizes",
    "stage_shard_summary",
]
