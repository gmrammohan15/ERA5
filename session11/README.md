# Session 11 — Optimizer and Learning-Rate Experiments

This submission implements the Session 11 assignment from
`Session11_transcript.md`. It reuses the deterministic Session 10 TinyGPT and
produces Adam verification tables, bias-correction traces, per-layer
update-to-weight ratios, tuned cosine/WSD comparisons, and width/LR sweeps.

Run from the repository root:

```bash
python session11/optimizer_harness.py
```

Outputs are written to `session11/artifacts/` and the generated explanation is
written to `session11/REPORT.md`.

The schedule experiments run for 300 steps and use step 200 as the primary
comparison checkpoint. The pilot LR grid is followed by three-seed reruns of
the selected cosine/WSD settings. Widths 256, 512, and 1,024 are swept and a
log-linear extrapolation recommends a learning rate for width 4,096.
