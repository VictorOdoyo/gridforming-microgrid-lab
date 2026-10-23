"""Regenerate coupled-model evidence and sampled-control maps for repository documentation."""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from gridlab.converter.delay_study import delay_study
from gridlab.lab.case import run_case
from gridlab.lab.cases import dc_step, hybrid_cloud, hybrid_restart
from gridlab.lab.config_io import case_dict
from gridlab.lab.dc_convergence import dc_convergence
from gridlab.lab.metrics import summarize
from gridlab.lab.observer_study import observer_study
from gridlab.lab.plotting import plot_case
from gridlab.provenance import provenance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=Path(__file__).resolve().parents[1] / "docs" / "results" / "physical"
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    records = {}
    for factory in (dc_step, hybrid_restart, hybrid_cloud):
        case = factory()
        trace = run_case(case)
        plot_case(case, trace, args.output / f"{case.name}.png")
        records[case.name] = {
            "case": case_dict(case),
            "metrics": summarize(case, trace),
            "provenance": provenance(case),
        }
    periods = (0.000025, 0.00005, 0.0001, 0.0002, 0.0005)
    delays = (0, 1, 2, 3)
    rows = delay_study(periods, delays)
    radius = np.array([row["spectral_radius"] for row in rows]).reshape(len(periods), len(delays))
    fig, ax = plt.subplots(figsize=(8, 5), layout="constrained")
    im = ax.imshow(radius, origin="lower", aspect="auto", cmap="RdYlGn_r", vmin=0.95, vmax=1.2)
    ax.set_xticks(range(len(delays)), [str(d) for d in delays])
    ax.set_yticks(range(len(periods)), [f"{p * 1e6:g}" for p in periods])
    for i in range(len(periods)):
        for j in range(len(delays)):
            ax.text(j, i, f"{radius[i, j]:.4f}", ha="center", va="center", color="black")
    ax.set_xlabel("Command delay [control samples]")
    ax.set_ylabel("Control period [microseconds]")
    ax.set_title("Local sampled cascade spectral radius — stable below 1")
    fig.colorbar(im, ax=ax, label="Spectral radius")
    fig.savefig(args.output / "sample-delay.png", dpi=150)
    plt.close(fig)
    records["sample-delay"] = rows
    records["dc-convergence"] = dc_convergence()
    records["observer"] = observer_study()
    (args.output / "measurements.json").write_text(
        json.dumps(records, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {k: v["metrics"] for k, v in records.items() if isinstance(v, dict) and "metrics" in v}, indent=2
        )
    )


if __name__ == "__main__":
    main()
