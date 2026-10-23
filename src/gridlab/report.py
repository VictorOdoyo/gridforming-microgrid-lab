"""A report bundle contains original arrays, case, metrics, figure, and provenance."""

import hashlib
import json
from html import escape
from pathlib import Path

from .config_io import save_case
from .csv_export import export_csv
from .plotting import plot_result
from .provenance import provenance
from .storage import save_result
from .summary import summarize


def write_report(case, result, directory):
    if abs(float(result.time[-1]) - case.duration) > 1e-9:
        raise ValueError("report case duration does not match saved trajectory")
    output = Path(directory)
    output.mkdir(parents=True, exist_ok=True)
    metrics = summarize(result)
    save_case(case, output / "case.json")
    save_result(result, output / "trace.npz")
    export_csv(result, output / "trace.csv")
    plot_result(result, output / "response.png", case.description, case.events)
    plot_result(result, output / "response.svg", case.description, case.events)
    for name, value in (
        ("metrics.json", metrics),
        ("provenance.json", {**provenance(case), "solver_options": result.solver_options}),
    ):
        (output / name).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    rows = "".join(f"<tr><th>{escape(k)}</th><td>{escape(str(v))}</td></tr>" for k, v in metrics.items())
    events = "".join(
        f"<li>{e.time:g} s: {escape(e.kind)}; target {e.target}; value {e.value:g}</li>" for e in case.events
    )
    html = f"""<!doctype html><html lang="en"><meta charset="utf-8">
<title>{escape(case.name)} — Grid-forming Microgrid Lab</title>
<style>body{{font:16px system-ui;max-width:1100px;margin:3rem auto;padding:0 1rem}}
img{{width:100%}}th,td{{text-align:left;padding:.35rem .7rem;border-bottom:1px solid #ddd}}
th{{font-weight:500}}code{{background:#eee;padding:.15rem}}</style>
<h1>{escape(case.name)}</h1><p>{escape(case.description)}</p>
<p>Balanced phasor simulation. Source frequencies describe internal control oscillators.
Power and RMS voltage use the common system per-unit base.</p>
<img src="response.png" alt="Frequency, voltage, active power, and source current versus time">
<h2>Metrics</h2><table>{rows}</table><h2>Scheduled events</h2><ul>{events}</ul>
<p><a href="case.json">Case</a> · <a href="trace.csv">CSV</a> ·
<a href="trace.npz">NumPy arrays</a> · <a href="provenance.json">Provenance</a> ·
<a href="response.svg">Vector figure</a></p></html>"""
    (output / "index.html").write_text(html, encoding="utf-8")
    names = (
        "case.json",
        "trace.npz",
        "trace.csv",
        "response.png",
        "response.svg",
        "metrics.json",
        "provenance.json",
        "index.html",
    )
    manifest = {name: hashlib.sha256((output / name).read_bytes()).hexdigest() for name in names}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return metrics
