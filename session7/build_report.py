from __future__ import annotations

from collections import defaultdict
import html
import json
import math
from pathlib import Path
import statistics

from session7.src.artifacts import ARTIFACT_DIR


ROOT = Path(__file__).resolve().parent
REPORT_DIR = ROOT / "report"


def _load(name: str) -> dict | None:
    path = ARTIFACT_DIR / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def _esc(value) -> str:
    return html.escape(str(value))


def _number(value, digits=3) -> str:
    if value is None:
        return "—"
    if isinstance(value, int):
        return f"{value:,}"
    return f"{float(value):.{digits}f}"


def _bytes(value) -> str:
    if value is None:
        return "—"
    value = float(value)
    units = ["B", "KiB", "MiB", "GiB"]
    index = 0
    while value >= 1024 and index < len(units) - 1:
        value /= 1024
        index += 1
    return f"{value:.2f} {units[index]}"


def _aggregate(lm: dict | None) -> dict[str, dict]:
    if not lm:
        return {}
    grouped: dict[str, list[dict]] = defaultdict(list)
    for run in lm.get("runs", []):
        grouped[run["architecture"]].append(run)
    result: dict[str, dict] = {}
    for architecture, runs in grouped.items():
        def mean(path):
            values = []
            for run in runs:
                value = run
                for key in path:
                    value = value[key]
                values.append(float(value))
            return statistics.mean(values)

        def stdev(path):
            values = []
            for run in runs:
                value = run
                for key in path:
                    value = value[key]
                values.append(float(value))
            return statistics.stdev(values) if len(values) > 1 else 0.0

        result[architecture] = {
            "runs": len(runs),
            "head_parameters": int(runs[0]["head_parameters"]),
            "total_parameters": int(runs[0]["total_parameters"]),
            "nll": mean(("validation", "overall", "mean_token_nll")),
            "nll_sd": stdev(("validation", "overall", "mean_token_nll")),
            "accuracy": mean(("test", "overall", "exact_accuracy")),
            "beam_accuracy": mean(("test", "beam_exact_accuracy")),
            "valid_utf8": mean(("test", "overall", "valid_utf8_rate")),
            "known_vocab": mean(("test", "overall", "known_vocab_rate")),
            "short_nll": mean(("validation", "short_tokens_only", "mean_token_nll")),
            "memory": max(int(run["test"]["peak_eval_logits_bytes"]) for run in runs),
            "latency": mean(("test", "greedy_latency_ms_per_token_p50")),
            "throughput": statistics.mean(float(run["training_tokens_per_second"]) for run in runs),
        }
    return result


def _line_svg(runs: list[dict]) -> str:
    if not runs:
        return '<div class="empty">No training curves yet.</div>'
    width, height, pad = 760, 240, 36
    colors = {"vocabulary": "#2f6fed", "parallel_byte": "#f59e0b", "autoregressive_byte": "#10b981"}
    points_by_name = []
    max_step = max(point["tokens"] for run in runs for point in run.get("curve", []))
    losses = [point["loss"] for run in runs for point in run.get("curve", [])]
    min_loss, max_loss = min(losses), max(losses)
    span = max(max_loss - min_loss, 1e-6)
    for run in runs:
        points = []
        for point in run.get("curve", []):
            x = pad + point["tokens"] / max_step * (width - 2 * pad)
            y = pad + (max_loss - point["loss"]) / span * (height - 2 * pad)
            points.append(f"{x:.1f},{y:.1f}")
        points_by_name.append(
            f'<polyline points="{" ".join(points)}" fill="none" stroke="{colors.get(run["architecture"], "#888")}" stroke-width="2" opacity=".7"/>'
        )
    return (
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="Training loss curves">'
        f'<line x1="{pad}" y1="{height-pad}" x2="{width-pad}" y2="{height-pad}" stroke="#d7dce3"/>'
        f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{height-pad}" stroke="#d7dce3"/>'
        + "".join(points_by_name)
        + f'<text x="{pad}" y="18" font-size="11" fill="#677">loss {max_loss:.2f}</text>'
        + f'<text x="{pad}" y="{height-8}" font-size="11" fill="#677">0 tokens</text>'
        + f'<text x="{width-pad-90}" y="{height-8}" font-size="11" fill="#677">{max_step:,} tokens</text>'
        + "</svg>"
    )


def build() -> Path:
    analysis = _load("data_analysis.json")
    reconstruction = _load("reconstruction_results.json")
    lm = _load("language_model_results.json")
    aggregate = _aggregate(lm)
    profile = (lm or reconstruction or analysis or {}).get("profile", "pending")

    rows = []
    order = ("vocabulary", "parallel_byte", "autoregressive_byte")
    labels = {
        "vocabulary": "Vocabulary head",
        "parallel_byte": "Parallel byte",
        "autoregressive_byte": "K-AR",
    }
    for name in order:
        item = aggregate.get(name)
        if not item:
            continue
        rows.append(
            "<tr>"
            f"<th>{labels[name]}</th>"
            f"<td>{item['head_parameters']:,}</td>"
            f"<td>{item['nll']:.3f} ± {item['nll_sd']:.3f}</td>"
            f"<td>{item['accuracy']:.2%}</td>"
            f"<td>{item['beam_accuracy']:.2%}</td>"
            f"<td>{item['valid_utf8']:.2%}</td>"
            f"<td>{_bytes(item['memory'])}</td>"
            f"<td>{item['latency']:.3f} ms</td>"
            "</tr>"
        )

    criteria = []
    if "vocabulary" in aggregate and "autoregressive_byte" in aggregate:
        base = aggregate["vocabulary"]
        kar = aggregate["autoregressive_byte"]
        checks = [
            ("≥8× fewer head parameters", base["head_parameters"] / kar["head_parameters"] >= 8, base["head_parameters"] / kar["head_parameters"]),
            ("≥4× lower peak logits memory", base["memory"] / max(1, kar["memory"]) >= 4, base["memory"] / max(1, kar["memory"])),
            ("Validation NLL within 10%", kar["nll"] <= base["nll"] * 1.10, kar["nll"] / max(base["nll"], 1e-9)),
            ("Valid UTF-8 ≥99%", kar["valid_utf8"] >= 0.99, kar["valid_utf8"]),
            ("Accuracy within 3 points", kar["accuracy"] >= base["accuracy"] - 0.03, kar["accuracy"] - base["accuracy"]),
            ("Greedy latency within 5×", kar["latency"] <= base["latency"] * 5, kar["latency"] / max(base["latency"], 1e-9)),
        ]
        if reconstruction:
            kar_reconstruction = next(
                model
                for model in reconstruction["result"]["models"]
                if model["architecture"] == "autoregressive_byte"
            )
            clean_short = kar_reconstruction["noise_results"]["0.0"]["short_tokens"]["exact_accuracy"]
            checks.insert(
                2,
                (
                    "Clean ≤32-byte reconstruction ≥99%",
                    clean_short >= 0.99,
                    clean_short,
                ),
            )
        for label, passed, value in checks:
            criteria.append(
                f'<li class="{"pass" if passed else "fail"}"><span>{"PASS" if passed else "NOT MET"}</span>{_esc(label)} <small>({_number(value)})</small></li>'
            )
    else:
        criteria.append('<li class="pending"><span>PENDING</span>Run the language-model experiment.</li>')

    reconstruction_rows = []
    if reconstruction:
        for model in reconstruction["result"]["models"]:
            clean = model["noise_results"].get("0.0", {})
            noisy = model["noise_results"].get("0.05", {})
            reconstruction_rows.append(
                "<tr>"
                f"<th>{labels.get(model['architecture'], model['architecture'])}</th>"
                f"<td>{model['head_parameters']:,}</td>"
                f"<td>{_number(clean.get('exact_accuracy'))}</td>"
                f"<td>{_number(clean.get('short_tokens', {}).get('exact_accuracy'))}</td>"
                f"<td>{_number(noisy.get('exact_accuracy'))}</td>"
                f"<td>{_number(noisy.get('codebook_cosine_accuracy'))}</td>"
                "</tr>"
            )

    observed_rows = []
    if analysis:
        for language, values in analysis["observed_token_lengths"].items():
            observed_rows.append(
                f"<tr><th>{language.upper()}</th><td>{values['tokens']:,}</td>"
                f"<td>{values['over_32_tokens']:,}</td><td>{values['over_32_fraction']:.2%}</td>"
                f"<td>{values['maximum_bytes']}</td></tr>"
            )

    curves = _line_svg((lm or {}).get("runs", []))
    raw_json = html.escape(json.dumps({"analysis": analysis, "reconstruction": reconstruction, "lm": lm}, ensure_ascii=False))
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Reverse Kronecker · Problem 5 Evidence</title>
<style>
:root{{--bg:#f5f7fa;--panel:#fff;--ink:#172033;--muted:#667085;--line:#dce2ea;--blue:#2f6fed;--green:#0d8f68;--amber:#b76e00;--red:#b42318}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,Segoe UI,sans-serif}}
.wrap{{max-width:1060px;margin:auto;padding:42px 22px 80px}} h1{{font-size:38px;letter-spacing:-.035em;margin:4px 0 8px}} h2{{font-size:21px;margin:0 0 14px}} p{{color:var(--muted)}}
.kicker{{font-size:12px;letter-spacing:.13em;text-transform:uppercase;color:var(--blue);font-weight:750}} .badge{{display:inline-block;padding:4px 10px;border-radius:99px;background:#e8efff;color:#2459c4;font-size:12px;font-weight:700}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:24px 0}} .card,section{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:22px;box-shadow:0 5px 18px rgba(23,32,51,.04)}} section{{margin-top:18px}} .big{{font-size:29px;font-weight:760}} .label{{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.07em}}
table{{border-collapse:collapse;width:100%;font-size:13px}} th,td{{padding:10px;border-bottom:1px solid var(--line);text-align:right}} th:first-child,td:first-child{{text-align:left}} thead th{{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.05em}}
ul.criteria{{list-style:none;padding:0;margin:0;display:grid;gap:8px}} .criteria li{{padding:10px 12px;border-radius:9px;background:#f5f7fa}} .criteria span{{display:inline-block;width:74px;font-size:11px;font-weight:800}} .pass span{{color:var(--green)}} .fail span{{color:var(--red)}} .pending span{{color:var(--amber)}} small{{color:var(--muted)}}
.flow{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}} .node{{border:1px solid var(--line);border-radius:10px;padding:9px 12px;background:#f9fbfd}} .arrow{{color:var(--blue);font-weight:800}} svg{{width:100%;height:auto}} .empty{{color:var(--muted);padding:30px;text-align:center}} code{{background:#eef2f7;padding:2px 5px;border-radius:5px}} footer{{text-align:center;color:var(--muted);font-size:12px;margin-top:30px}}
@media(max-width:760px){{.grid{{grid-template-columns:1fr}} table{{display:block;overflow:auto}} h1{{font-size:31px}}}}
</style></head><body><div class="wrap">
<div class="kicker">ERA V5 · Session 7</div><h1>Reverse Kronecker</h1>
<p>Can a structured byte decoder replace the vocabulary-sized output head?</p><span class="badge">{_esc(profile)} evidence profile</span>
<div class="grid">
<div class="card"><div class="label">Vocabulary</div><div class="big">{_number((analysis or {}).get('vocabulary_items'))}</div><p>Session 2 multilingual BPE</p></div>
<div class="card"><div class="label">K-AR head parameters</div><div class="big">{_number(aggregate.get('autoregressive_byte', {}).get('head_parameters'))}</div><p>Independent of vocabulary size</p></div>
<div class="card"><div class="label">Runs completed</div><div class="big">{len((lm or {}).get('runs', []))}</div><p>Shared input and Transformer body</p></div>
</div>
<section><h2>Claim under test</h2><div class="flow"><div class="node">Transformer state</div><div class="arrow">→</div><div class="node">byte 1</div><div class="arrow">→</div><div class="node">byte 2 …</div><div class="arrow">→</div><div class="node">EOS</div></div>
<p>K-AR factorizes token probability over bytes. The standard head, parallel byte head, and K-AR receive identical K32 inputs, data order, and Transformer initialization.</p></section>
<section><h2>Success contract</h2><ul class="criteria">{''.join(criteria)}</ul></section>
<section><h2>Language-model comparison</h2><table><thead><tr><th>Architecture</th><th>Head params</th><th>Validation NLL</th><th>Greedy exact</th><th>Beam exact</th><th>Valid UTF-8</th><th>Peak logits</th><th>Greedy latency</th></tr></thead><tbody>{''.join(rows) or '<tr><td colspan="8">Run the LM experiment to populate this table.</td></tr>'}</tbody></table></section>
<section><h2>Training curves</h2>{curves}</section>
<section><h2>Projected-code reconstruction</h2><table><thead><tr><th>Decoder</th><th>Head params</th><th>Clean exact</th><th>Clean ≤32</th><th>σ=.05 exact</th><th>Codebook σ=.05</th></tr></thead><tbody>{''.join(reconstruction_rows) or '<tr><td colspan="6">Run reconstruction to populate this table.</td></tr>'}</tbody></table><p>Codebook cosine search stores every vocabulary vector and is an accuracy baseline, not a head-free solution.</p></section>
<section><h2>The shared K32 long-token limitation</h2><table><thead><tr><th>Language</th><th>Tokens</th><th>&gt;32</th><th>Share</th><th>Maximum bytes</th></tr></thead><tbody>{''.join(observed_rows) or '<tr><td colspan="5">Run analysis to populate this table.</td></tr>'}</tbody></table><p>These tokens remain in all runs. The report also presents ≤32-byte-only metrics to isolate the output mechanism.</p></section>
<section><h2>Interpretation rules</h2><p>A smaller head is not automatically a better language model. Reconstruction is not next-token prediction. Generating a new byte string does not imply learned knowledge. Deployment superiority additionally requires acceptable serial decoding latency.</p></section>
<details><summary>Embedded evidence JSON</summary><pre id="raw">{raw_json}</pre></details>
<footer>Generated from local reproducible artifacts · no external scripts or services</footer>
</div></body></html>"""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / "index.html"
    path.write_text(document, encoding="utf-8")
    (REPORT_DIR / "netlify.toml").write_text('[build]\npublish = "."\n', encoding="utf-8")
    print(path)
    return path


if __name__ == "__main__":
    build()
