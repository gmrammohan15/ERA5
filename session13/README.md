# Session 13 — Reversible language-model training

Train a roughly 20M-parameter causal LM for 50M tokens, compare ordinary Transformer training with two reversible variants at one fixed batch size, then repeat the better reversible variant at its maximum safe batch size.

## What is implemented

- **Baseline:** pre-norm causal Transformer with tied GPT-2 token/output embeddings.
- **Midpoint:** reversible two-step recurrence with an Euler bootstrap and activation reconstruction in the custom backward pass.
- **Hamiltonian symplectic Euler:** reversible position/momentum updates, also reconstructed during backward.
- **Data:** streaming FineWeb-Edu `sample-10BT`, GPT-2 BPE tokenization, a deterministic document-hash validation split, and packed token windows. The train stream is cut at exactly 50,000,000 tokens; each variant sees that same token stream and 250,000 held-out validation tokens.
- **Matched settings:** 256-token context, identical initialization seed, AdamW, no dropout, and zero weight decay. The default architecture has 20,039,680 trainable parameters.

The reversible architectures are based on the midpoint and Hamiltonian symplectic-Euler constructions described in [Reversing Large Language Models for Efficient Training and Fine-Tuning](https://arxiv.org/abs/2512.02056). The paper also discusses leapfrog; this assignment run focuses on the two variants named in the session transcript. Plain residual Euler is not reversible, so it is not used as a reversible baseline.

## Local design checks

Requires PyTorch 2.x. Run:

```bash
python session13/reversible_lm.py --smoke
```

This checks the model parameter target, causal masking and next-token loss, reconstruction error for both reversible methods, custom backward gradients against ordinary autograd, and one optimizer update. It does not download data or claim GPU performance.

## Run in Google Colab

1. Open [`session13_colab.ipynb`](session13_colab.ipynb) in Colab and select a CUDA GPU runtime.
2. Make the repository version of `reversible_lm.py` available to the notebook. The first cell clones the public repository; if your changes have not been pushed yet, upload `reversible_lm.py` to `/content/ERA5/session13/` after the clone, or push the files before opening the notebook.
3. Run the notebook from the top. It caches tokenized data and results under `MyDrive/session13_artifacts` when Drive is mounted.
4. The notebook calibrates the largest baseline-safe batch, runs baseline/midpoint/symplectic-Euler at that fixed batch, selects the reversible method with the lower final validation loss, calibrates its maximum safe batch, and runs that final comparison.

All four training runs process 50M tokens. Runtime varies by Colab GPU and its current load. Batch calibration uses one probe update per tested batch and keeps at least 12% of reported GPU memory unallocated as headroom. The search is capped at 1,024 sequences; the report flags if that cap is reached instead of claiming a hardware limit beyond the search range.

## Outputs

The output folder contains:

- `REPORT.md` — comparison table with final train/validation loss, tokens/s, and peak GPU memory.
- `session13_results.json` — run configuration, device, calibration probes, and per-run loss traces.
- `baseline_fixed.json`, `midpoint_fixed.json`, `symplectic_euler_fixed.json`, and the selected maximum-batch run JSON.
- One loss CSV per run and `loss_curves.png`.
- `fineweb_edu_gpt2_tokens.pt` — reusable tokenized train/validation streams.

Throughput measures the training loop only, after CUDA synchronization; dataset preparation and validation are excluded. Peak allocated and reserved memory use PyTorch CUDA counters. Cost is not calculated because runtime tier and billing differ by account; add the actual Colab tier and billed amount to the report if comparing cost.

## Dependencies

The notebook installs `datasets`, `tiktoken`, and `matplotlib`. PyTorch 2.x is needed for scaled dot-product attention and the CUDA memory counters.
