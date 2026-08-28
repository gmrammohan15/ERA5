# Session 9 — Loss Harness and Output Heads

This submission implements the Session 9 assignment from the lecture transcript. The notebook is [notebook.ipynb](notebook.ipynb); the executable harness is [loss_harness.py](loss_harness.py).

## Run

Open `notebook.ipynb` in Google Colab and run all cells. The corpus is embedded, so there is no dataset download. If the notebook is opened directly in Colab, it fetches the adjacent harness from this repository's `main` branch.

The local equivalent is:

```bash
python session9/loss_harness.py
```

## Configuration

The experiment uses a deterministic character-level causal Transformer:

| Setting | Value |
|---|---:|
| vocabulary size | 36 |
| block size | 64 |
| hidden dimension | 96 |
| attention heads | 4 |
| Transformer layers | 2 |
| seed | 9 |

Characters are used so the shift check can show the actual strings, including spaces and special `<eos>`/`<pad>` tokens.

## Part 1 results

The requested Part 1 measurements are listed below. The memory benchmark has three reported values (ordinary, chunked, and ratio), so all required sub-measurements are included rather than collapsed into one number.

| Measurement | Result |
|---|---:|
| padding positions before mask | 116 |
| padding positions after mask | 85 |
| padding loss before mask | 2.628974 |
| padding loss after mask | 3.583519 |
| packed-document loss before boundary mask | 3.568511 |
| packed-document loss after boundary mask | 3.583519 |
| untrained perplexity | 36.000000 |
| tied unique model parameters | 233,472 |
| untied unique model parameters | 236,928 |
| ordinary CE peak memory (recorded local CPU run) | 99.281 MiB |
| chunked CE peak memory (recorded local CPU run) | 50.516 MiB |
| ordinary/chunked memory ratio | 1.965x |

The vocabulary has 36 classes, so an exactly uniform untrained head has loss `ln(36) = 3.583519` and perplexity 36. The head is zero-initialized for this sanity check; this makes the expected baseline explicit rather than relying on random initialization.

Padding reduces the number of contributing targets from 116 to 85. The diagnostic logits deliberately make `<pad>` easy to predict, so including padding produces an artificially low loss. The packed sequence contains one cross-document transition, `<eos> -> 'A'`; masking it removes that transition from the loss. The loss rises because the easy boundary example no longer contributes.

Weight tying reuses the input embedding matrix transposed, adding no independent head parameters. The reported tied total already includes the input embedding once. The untied head adds `V × D = 36 × 96 = 3,456` parameters.

The chunked implementation computes the same cross-entropy one slice of positions at a time. Its loss matches ordinary CE to floating-point precision while using about 1.965 times less measured peak memory in the recorded local CPU run. Memory is environment-sensitive: the notebook prints the actual device and measurement method; CUDA runs use `max_memory_allocated`, while CPU runs use isolated child-process peak RSS.

## Part 2: t+2 output head

Both heads receive the same hidden states. Head 1 predicts `t+1`; head 2 predicts `t+2`.

| Measurement | Loss |
|---|---:|
| head t+1, final step | 0.243069 |
| head t+2, final step | 0.267971 |
| summed final loss | 0.511040 |

Both losses decrease during training. The t+2 loss remains slightly higher: it predicts a farther token from the same context and cannot use the ground-truth t+1 token as an additional input. That makes the target less locally determined and explains the slower/higher curve observed in this run.

## Reading-based correctness demonstration

The notebook also constructs a deliberately copy-biased diagnostic. Its loss is:

| Target alignment | Loss |
|---|---:|
| correct shifted t+1 target | 8.011672 |
| incorrect same-position target | 0.011673 |

The second number is deceptively good because the diagnostic predicts the token it was given. It is not next-token prediction. The printed string table makes the required one-position shift visible without asking the reader to decode integer ids.
