# Session 12 — Simulating ZeRO-1, ZeRO-2, and ZeRO-3

Repository: [ERA5](https://github.com/gmrammohan15/ERA5)

This submission implements the Session 12 assignment: create a simple 32-GPU setup, run a demo model on it, simulate ZeRO-1/2/3, and show how memory and computation/communication change.

## What this demonstrates

The project uses 32 **logical virtual GPU ranks**. It runs on CPU, so it does not pretend that a laptop has 32 physical GPUs. The logical ranks are enough to make the ownership rules visible and reproducible:

- ZeRO-0/data parallelism: every rank stores the complete model, gradients, FP32 master weights, and Adam moments.
- ZeRO-1: optimizer states are sharded; every rank still has the full parameters and gradients.
- ZeRO-2: optimizer states and gradients are sharded.
- ZeRO-3: parameters, gradients, and optimizer states are all sharded. A rank temporarily gathers the parameters needed for a layer, then releases them.

The toy model is a two-layer MLP. The real PyTorch step is intentionally small enough for a laptop or Colab. Memory and communication are calculated explicitly so the scaling effect is easier to see than it would be in a noisy hardware benchmark.

## Main files

- [`session12_zero_simulation.ipynb`](session12_zero_simulation.ipynb): runnable walkthrough and plots.
- [`zero_simulator.py`](zero_simulator.py): reusable simulator and correctness checks.
- [`generate_artifacts.py`](generate_artifacts.py): regenerates the CSV, JSON, and plot used here.
- [`artifacts/zero_results.csv`](artifacts/zero_results.csv): experiment table.
- [`artifacts/memory_and_communication.png`](artifacts/memory_and_communication.png): summary plot.

## Run it

```bash
cd session12
python -m pip install -r requirements.txt
python generate_artifacts.py
jupyter notebook session12_zero_simulation.ipynb
```

The notebook can run without CUDA. It creates 32 logical ranks in the `VirtualCluster` model; the default execution is sequential and deterministic so it is reliable in a notebook. The optional multiprocessing idea is deliberately not required for the learning result because CPU process startup and scheduling would obscure the ZeRO accounting.

## Memory accounting

For Adam-style training, the replicated state is approximately 16 bytes per parameter:

```text
2 bytes  low-precision parameters used for arithmetic
2 bytes  low-precision gradients
4 bytes  FP32 master weights
4 bytes  Adam first moment
4 bytes  Adam second moment
```

With `P` parameters and `N=32` ranks, the idealized per-rank model-state memory is:

| Strategy | Per-rank state |
|---|---:|
| ZeRO-0 | `16P` |
| ZeRO-1 | `4P + 12P/N` |
| ZeRO-2 | `2P + 14P/N` |
| ZeRO-3 | `16P/N`, plus temporary layer buffers |

Activations are reported separately because they depend on batch size, sequence length, and the model architecture. The notebook also shows that an uneven parameter or layer count cannot always divide perfectly across ranks; one or more ranks may own a slightly larger shard.

## Communication and computation

The arithmetic performed by the toy model is kept constant across the comparison. The distributed behavior is represented by ownership and collective communication:

- ZeRO-0 and ZeRO-1 need gradient synchronization.
- ZeRO-2 uses gradient reduce-scatter, with optimizer updates performed on the owner rank.
- ZeRO-3 additionally all-gathers parameters before the relevant layer computation.

The notebook reports estimated collective bytes, modeled communication time, and a relative step-cost estimate using configurable bandwidth and arithmetic throughput. The example uses 5 GB/s deliberately so the communication effect is visible for a tiny toy model; changing it to 450 GB/s gives an NVLink-like sensitivity check. These are not claims about CPU copy speed or a real GPU benchmark. The point is the relationship: ZeRO-3 gives the largest memory reduction, but it introduces more parameter traffic and therefore can be slower when communication is the bottleneck.

## My understanding

I understand ZeRO as removing redundant *stored state* from ordinary data parallelism. In ordinary data parallelism, every GPU receives different data but still keeps a complete copy of the model, gradients, and optimizer state. That makes the GPUs agree after gradient synchronization, but it also means the same large state is replicated many times.

ZeRO-1 starts with the largest easy win: optimizer state is partitioned across ranks. ZeRO-2 partitions gradients as well, so each rank stores less temporary training state. ZeRO-3 partitions the parameters themselves. That is why ZeRO-3 can make a much larger model fit, but it also has to materialize and communicate parameter shards during forward and backward computation.

The model's final mathematical update can remain equivalent across the stages. The trade-off is not “better model quality versus worse model quality”; it is memory capacity, communication, temporary peak memory, and step time. If computation takes a long time, communication can be hidden more easily. If the model is small or the interconnect is slow, the additional ZeRO-3 communication can waste more time than it saves.

## Limitations

This is an educational simulator, not DeepSpeed or FSDP. It does not benchmark physical GPUs, implement a real NCCL process group, model activation checkpointing, or include CPU/NVMe offload. Its purpose is to make the lecture's state partitioning and communication trade-offs explicit and testable on a normal CPU machine.
