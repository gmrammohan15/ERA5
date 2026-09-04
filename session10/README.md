# ERA5 Session 10 — Training Loop Truth Harness

This assignment turns a small real training loop into an instrumented experiment. It follows the Session 10 requirements in [the transcript](Session10_transcripts.md): print tensor shapes, verify one gradient numerically, expose the variable-length gradient-accumulation bug, log gradient norms, calculate MFU, and decode `0.1` in FP32, BF16, and FP8 E4M3.

The model is a self-contained, character-level, two-block causal GPT. Its structure is deliberately close to [Karpathy's nanoGPT](https://github.com/karpathy/nanoGPT), while remaining runnable without downloading a repository or dataset.

## Run

From the repository root:

```bash
python session10/training_harness.py
```

Optional GPU MFU calculation:

```bash
python session10/training_harness.py --device cuda --peak-tflops 989
```

The local baseline is CPU-only. Without `--peak-tflops`, the harness reports achieved estimated TFLOP/s and explicitly marks conventional MFU unavailable.

## Outputs

- `REPORT.md` — generated explanation and measured results.
- `artifacts/results.json` — shape trace, parameter inventory, checks, MFU fields, and floating-point decoding.
- `artifacts/training_metrics.csv` — per-step losses, gradient norms, and token counts.
- `artifacts/accumulation_comparison.png` — naive and correct accumulation curves together.
- `artifacts/training_diagnostics.png` — gradient norm and fixed-probe loss over steps.

## Interpretation

For micro-batches with `n1` and `n2` valid tokens, the correct loss/gradient combination is token-weighted:

```text
(n1 * loss1 + n2 * loss2) / (n1 + n2)
```

The naive average of `loss1` and `loss2` gives equal weight to examples rather than tokens. With different lengths, it is a different optimization problem.

The MFU estimate follows the lecture's rough training-work rule:

```text
estimated FLOPs = 6 * parameter_count * processed_tokens
MFU = achieved FLOP/s / hardware peak FLOP/s
```

The `6NT` estimate is approximate and omits detailed attention, softmax, normalization, data loading, and runtime overhead.

For `0.1`, the expected rounded encodings are:

| Format | Bits | Decoded value |
|---|---|---:|
| FP32 | `0 01111011 10011001100110011001101` | `0.10000000149` |
| BF16 | `0 01111011 1001101` | `0.10009765625` |
| FP8 E4M3 | `0 0011 101` | `0.1015625` |

BF16 is the default choice for this small training experiment because its exponent range is similar to FP32 and it preserves small gradients better than a raw FP8 cast. Production FP8 training requires scaling; NVIDIA's [Transformer Engine documentation](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/features/low_precision_training/fp8_current_scaling/fp8_current_scaling.html) describes E4M3/E5M2 and tensor scaling.
