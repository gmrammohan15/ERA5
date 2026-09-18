"""Generate small, committed artifacts used by the Session 12 README."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt

from zero_simulator import (
    STAGES,
    build_experiment_rows,
    correctness_check,
    human_bytes,
    mlp_parameter_count,
)


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)


def main() -> None:
    parameters = mlp_parameter_count(64, 1024, 64)
    rows = build_experiment_rows(
        parameters=parameters,
        world_size=32,
        bandwidth_gbps=5.0,
        activation_bytes_per_rank=2 * 1024 * 1024,
        batch_size=128,
        input_dim=64,
        hidden_dim=1024,
        output_dim=64,
    )

    csv_path = ARTIFACTS / "zero_results.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "parameters": parameters,
        "world_size": 32,
        "correctness": correctness_check(),
        "memory": {
            row["stage"]: human_bytes(row["model_state_bytes_per_rank"])
            for row in rows
        },
    }
    (ARTIFACTS / "correctness.json").write_text(json.dumps(summary, indent=2))

    labels = ["ZeRO-0", "ZeRO-1", "ZeRO-2", "ZeRO-3"]
    state_mib = [row["model_state_bytes_per_rank"] / 2**20 for row in rows]
    comm_mib = [row["communication_total_bytes_per_rank"] / 2**20 for row in rows]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2), constrained_layout=True)
    axes[0].bar(labels, state_mib, color=["#6b7280", "#2563eb", "#059669", "#d97706"])
    axes[0].set_title("Model state per logical rank")
    axes[0].set_ylabel("MiB")
    axes[0].grid(axis="y", alpha=0.25)
    axes[1].bar(labels, comm_mib, color=["#6b7280", "#2563eb", "#059669", "#d97706"])
    axes[1].set_title("Modeled communication per step")
    axes[1].set_ylabel("MiB per rank")
    axes[1].grid(axis="y", alpha=0.25)
    axes[2].bar(labels, [row["estimated_step_ms"] for row in rows], color=["#6b7280", "#2563eb", "#059669", "#d97706"])
    axes[2].set_title("Estimated step cost")
    axes[2].set_ylabel("ms; 1 TFLOP/s assumption")
    axes[2].grid(axis="y", alpha=0.25)
    fig.suptitle(f"32 logical ranks, {parameters:,} parameters")
    fig.savefig(ARTIFACTS / "memory_and_communication.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
