"""Static laboratory report directories with full original evidence."""

import hashlib
import json
from html import escape
from pathlib import Path

from gridlab.provenance import provenance

from .config_io import case_dict, save_case
from .csv_export import export_csv
from .metrics import summarize
from .plotting import plot_case
from .storage import save_trace


def write_report(case, trace, directory):
    if (
        abs(trace.time[-1] - case.duration) > 1e-9
        and getattr(trace, "termination", "completed") == "completed"
    ):
        raise ValueError("completed trace horizon does not match its case")
    out = Path(directory)
    out.mkdir(parents=True, exist_ok=True)
    metrics = summarize(case, trace)
    metadata = {**provenance(case), "case": case_dict(case), "period_s": case.period_s}
    save_case(case, out / "case.json")
    save_trace(case.kind, trace, out / "trace.npz", metadata)
    export_csv(case, trace, out / "trace.csv")
    plot_case(case, trace, out / "response.png")
    plot_case(case, trace, out / "response.svg")
    for name, value in (("metrics.json", metrics), ("provenance.json", metadata)):
        (out / name).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    table = "".join(
        f"<tr><th>{escape(k)}</th><td>{escape(str(v))}</td></tr>"
        for k, v in metrics.items()
        if not isinstance(v, dict)
    )
    audit = escape(json.dumps(metrics.get("energy", {}), indent=2))
    html = f"""<!doctype html><html lang="en"><meta charset="utf-8">
<title>{escape(case.name)}</title>
<style>body{{font:16px system-ui;max-width:1100px;margin:3rem auto;padding:0 1rem}}
img{{width:100%}}th,td{{padding:.3rem;text-align:left;border-bottom:1px solid #ddd}}
pre{{background:#f3f4f6;padding:1rem;overflow:auto}}</style>
<h1>{escape(case.name)}</h1><p>{escape(case.description)}</p>
<p>Physical model: {escape(case.kind)}. Voltages and currents use SI units.
AC dq variables use peak amplitude; plots explicitly identify RMS quantities.</p>
<img src="response.png" alt="Physical experiment telemetry">
<h2>Performance</h2><table>{table}</table><h2>Energy audit</h2><pre>{audit}</pre>
<p><a href="case.json">Case</a> · <a href="trace.csv">CSV</a> ·
<a href="trace.npz">Original trace</a> · <a href="response.svg">SVG</a> ·
<a href="provenance.json">Provenance</a></p></html>"""
    (out / "index.html").write_text(html, encoding="utf-8")
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
    manifest = {n: hashlib.sha256((out / n).read_bytes()).hexdigest() for n in names}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return metrics
