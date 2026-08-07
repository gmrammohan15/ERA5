# ERA5 Assignments

> **Session 5 submission:** [V5 Mixture And Curriculum Plan](session5/README.md)

---

# Four Proofs · ERA5 Session 1

A single-page scrollytelling web app that **proves** the four foundational claims from
ERA5 Session 1 ("From Neural Networks to the Transformer"). Every claim is verified two ways:

1. **Offline (PyTorch):** trained in Python, exported to JSON, and checked by an automated
   acceptance eval before it ships. This is the polished "money shot" shown by default.
2. **Live (TensorFlow.js):** each proof also ships an interactive panel that trains a **real
   model in your browser**. Drag the sliders, flip the switches, hit Retrain, and watch the
   decision boundary re-form, the embeddings self-organize, or the generalization gap shrink.

Nothing on the page is hand-drawn.

> Deployed site: _add your Netlify URL here after deploying_

---

## The four proofs

| # | Claim | Verdict shown on the page | Lecture |
|---|-------|---------------------------|---------|
| **S1-1** | Activations exist for a reason | A single linear layer is stuck near chance (~54%) on two concentric rings; one ReLU hidden layer wraps the ring (~99%). Only the activation changed. | §3 The activation |
| **S1-2** | Depth without nonlinearity is a lie | 1 linear layer and 5 stacked linear layers give the same straight boundary; ReLU breaks the tie. The five weight matrices multiply out to a single 1×2 matrix (collapse error ~0). | §4 From one neuron to a network |
| **S1-3** | Embeddings learn similarity from nothing but next-token | Trained only to predict the next token in a toy grammar, the embedding table clusters same-category tokens (100% same-category nearest neighbors). Similarity was never supplied. | §7 Words as numbers |
| **S1-4** | Memorization vs generalization, and data closes the gap | At 20 samples the net memorizes (train→100%) while test lags — a large gap that collapses as the dataset grows to 2000. Same model, only the data grew. | §12 Data is everything |

---

## Requirements

- **Python 3.10+** with `torch`, `numpy`, `scikit-learn` (for the precompute + eval).
- **Node 18+** and **npm** (for the web app).

Install the Python side:

```bash
cd ml
pip install -r requirements.txt
```

Install the web side:

```bash
cd web
npm install
```

---

## Project structure

```
ERA5/
├── ml/                      # Python precompute + acceptance eval
│   ├── requirements.txt
│   ├── generate_all.py      # runs all four proofs, then eval.py
│   ├── eval.py              # acceptance harness (PASS/FAIL, exits nonzero on failure)
│   ├── proofs/
│   │   ├── s1_activations.py
│   │   ├── s1_depth.py
│   │   ├── s1_embeddings.py
│   │   └── s1_data.py
│   └── utils/
│       ├── common.py        # ring dataset, grid, training helpers
│       └── export.py        # JSON writer -> web/public/data/
├── web/                     # Vite + React + TypeScript + Tailwind scrollytelling site
│   ├── src/
│   │   ├── components/      # Hero, ProofSection, DecisionBoundary, EmbeddingScatter, MatrixProduct, LineChart, AnimatedNumber, controls
│   │   ├── proofs/          # Activations, Depth, Embeddings, DataGap
│   │   │   └── interactive/ # live TensorFlow.js panels (one per proof)
│   │   ├── ml/              # client ML: datasets.ts, train.ts (TFJS), useLiveRun.ts, rng.ts
│   │   ├── App.tsx, main.tsx, types.ts, useData.ts, index.css
│   ├── public/data/*.json   # generated artifacts (checked in so the site is self-contained)
│   ├── netlify.toml
│   └── package.json
└── README.md
```

---

## Design

- **Dark scrollytelling page.** A hero intro, then four stacked proof sections, then a closing
  callback to the lecture. Each section follows the same rhythm: **Claim → Build → visual → Proof verdict**.
- **Fixed color language.** Class 0 = amber (`#f59e0b`), class 1 = cyan (`#22d3ee`) everywhere.
  Decision-boundary heatmaps interpolate amber↔cyan by predicted probability, with a thin white
  zero-crossing isoline for the boundary itself.
- **Precomputed default + live interactivity.** The default visuals load instantly from baked JSON
  (no runtime ML, never fails in front of a viewer). Below each one, an interactive panel trains a
  real TensorFlow.js model client-side. Each panel only starts training when scrolled into view (so
  the page loads fast), and TensorFlow.js is split into its own cached chunk.
- **Rendering.** HTML5 Canvas for the decision-boundary heatmaps and point overlays; lightweight
  inline SVG for line charts, the embedding scatter, and the weight-matrix grids; Framer Motion for
  scroll reveals and count-up numbers.

### Interactive panels (live TensorFlow.js)

The client-side ML lives in `web/src/ml/`:

- `datasets.ts` — seeded generators (rings, moons, toy grammar) mirroring the Python.
- `train.ts` — TFJS training loops for each proof, yielding per-epoch updates (boundary grid,
  accuracy, embedding positions, loss curves) and cancelling cleanly on retrain/unmount.
- `useLiveRun.ts` — a React hook that streams training updates into state.

What you can control per proof:

- **S1-1:** toggle the ReLU hidden layer, hidden units, data noise, learning rate, epochs.
- **S1-2:** number of stacked layers (1–6), ReLU on/off, epochs — plus the live collapsed matrix.
- **S1-3:** learning rate, epochs, random seed — watch 2-D embeddings drift into clusters.
- **S1-4:** training set size (10–2000), noise, epochs — watch the train/test gap open and close.

---

## Implementation details

Each proof script trains small models and writes one JSON file into `web/public/data/`.

- **`s1_activations.py`** → `activations.json`. Generates ~300 points as two concentric noisy rings.
  Trains `Linear(2,1)+sigmoid` and `Linear(2,16)→ReLU→Linear(16,1)`. Exports the points, a 100×100
  probability grid per model, and final accuracies.
- **`s1_depth.py`** → `depth.json`. Same ring data. Trains 1 linear layer, 5 stacked linear layers
  (no activations, no bias), and 5 layers + ReLU. Exports boundaries/accuracies, the five weight
  matrices, their numeric product `W5·W4·W3·W2·W1` (a single 1×2 matrix), and the max error between
  the full stack and that single matrix over the grid.
- **`s1_embeddings.py`** → `embeddings.json`. Builds a toy grammar (`⟨animal⟩ ⟨verb⟩ ⟨animal|fruit⟩`)
  where same-category tokens are interchangeable, so they share next-token distributions. Trains an
  `Embedding → Linear → softmax` next-token model, projects the learned embeddings to 2D with PCA,
  and exports token coordinates, categories, cosine nearest neighbors, and the loss curve.
- **`s1_data.py`** → `data_gap.json`. A noisy two-moons problem with a fixed 2000-point held-out test
  set. Trains an over-parameterized MLP at train sizes 20/200/2000 (averaged over several random
  draws for a stable estimate), exporting train/test loss curves and the generalization gap vs size.

### JSON contracts

- `activations.json`: `{ points, grid, models: { linear, relu } }`, each model `{ prob[][], accuracy, loss }`.
- `depth.json`: `{ points, grid, models: { linear1, linear5, relu5 }, weightMatrices, weightShapes, collapsedProduct, collapseError, boundariesIdentical }`.
- `embeddings.json`: `{ tokens[], categoryColors, neighbors[], loss[], sameCategoryNNRate, exampleSentences[] }`.
- `data_gap.json`: `{ sizes[], runs[], gap[] }`.

---

## Run locally

From the repo root, generate the artifacts and run the eval:

```bash
cd ml
pip install -r requirements.txt
cd ..
python -m ml.generate_all
```

This writes the four JSON files into `web/public/data/` and prints a PASS/FAIL acceptance report.
Then start the web app:

```bash
cd web
npm install
npm run dev        # local preview at http://localhost:5173
npm run build      # production build into web/dist/
```

---

## Acceptance eval

The eval turns the four "proofs" into something automatically verifiable instead of eyeballed. It
loads the exported JSON, validates schemas (grid shape, values in `[0,1]`, no NaN/Inf), and asserts
per-claim numeric thresholds:

- **S1-1**: linear accuracy ≤ 0.70, ReLU ≥ 0.95, margin ≥ 0.30.
- **S1-2**: `|linear1 − linear5| ≤ 0.03` and both ≤ 0.70, ReLU5 ≥ 0.95, matrix collapse error < 1e-4, single 1×2 product.
- **S1-3**: same-category nearest-neighbor rate ≥ 0.80, intra-cluster distance < inter-cluster distance, loss decreased.
- **S1-4**: size-20 train accuracy ≥ 0.98 with gap ≥ 0.20, gap non-increasing with data, and shrinking by ≥ 0.15.

Run it on its own at any time:

```bash
python -m ml.eval        # exits 0 if all checks pass, 1 otherwise
```

It also runs automatically as the final step of `python -m ml.generate_all`, so an under-tuned run
fails loudly instead of shipping a weak proof.

---

## Deploying to Netlify

The site is a fully static build (`web/dist/`) with the data JSON baked in, so any static host works.
Two documented paths:

### Option 1 — Quick drag-and-drop (no Git needed)

1. Create a free account at <https://app.netlify.com/signup> (GitHub or email).
2. Build locally:
   ```bash
   cd web
   npm install
   npm run build
   ```
3. In the Netlify dashboard: **Add new site → Deploy manually**, then drag the `web/dist` folder onto
   the drop zone.
4. Netlify returns a permanent URL like `https://your-site.netlify.app`. Rename it under
   **Site settings → Change site name** for a cleaner link. Because the account persists the deploy,
   the link stays live.

### Option 2 — Git-connected continuous deploy (recommended for updates)

1. Push this repo to GitHub.
2. In Netlify: **Add new site → Import an existing project** and pick the repo.
3. Set:
   - **Base directory:** `web`
   - **Build command:** `npm run build`
   - **Publish directory:** `web/dist`
   (These are also captured in [`web/netlify.toml`](web/netlify.toml), so Netlify auto-detects them.)
4. Every push to the main branch triggers an automatic rebuild and redeploy. Optionally set a custom
   domain under **Domain settings**.

`web/netlify.toml`:

```toml
[build]
  base = "web"
  command = "npm run build"
  publish = "dist"
```

---

## Notes

- If you change the dataset or hyperparameters in `ml/`, re-run `python -m ml.generate_all` to
  regenerate the JSON (the eval will tell you if a claim no longer holds), then rebuild the web app.
- The generated JSON in `web/public/data/` is committed so the site is self-contained and reproducible
  even without running Python.
# ERA5
