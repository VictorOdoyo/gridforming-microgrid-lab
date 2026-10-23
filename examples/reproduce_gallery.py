"""Regenerate curated README figures and measured summaries from the installed package."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from gridlab.cases import island_recovery, load_step
from gridlab.daily_energy import daily_energy
from gridlab.events import run_events
from gridlab.plotting import plot_result
from gridlab.provenance import provenance
from gridlab.summary import summarize

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1]/"docs"/"results")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    measurements = {}
    for key, case in (("load-step-droop", load_step("droop")),
                      ("load-step-vsm", load_step("vsm")),
                      ("island-recovery-vsm", island_recovery("vsm"))):
        result = run_events(case.config, case.events, case.duration, sample_s=.02, max_step=.02)
        plot_result(result, args.output/f"{key}.png", case.description, case.events)
        measurements[key] = {"metrics": summarize(result), "provenance": provenance(case),
                             "solver_options": result.solver_options}
    energy = daily_energy()
    rows = energy["intervals"]
    hours = np.array([r["time_s"] for r in rows])/3600
    fig, axes = plt.subplots(2, 1, figsize=(11, 6), sharex=True, layout="constrained")
    for key, label in (("load_kw", "Load"), ("solar_kw", "Solar used"),
                       ("battery_kw", "Battery discharge (+) / charge (-)"), ("diesel_kw", "Diesel")):
        axes[0].step(hours, [r[key] for r in rows], where="post", label=label)
    axes[0].set_ylabel("Interval power [kW]")
    axes[0].legend(fontsize=8)
    axes[1].step(hours, [r["soc"] for r in rows], where="post")
    axes[1].set_ylabel("Battery state of charge")
    axes[1].set_xlabel("Time of day [h]")
    axes[1].set_ylim(0, 1)
    for ax in axes:
        ax.grid(alpha=.2)
    fig.suptitle("Separate daily solar / battery / diesel dispatch experiment")
    fig.savefig(args.output/"daily-energy.png", dpi=150)
    plt.close(fig)
    measurements["daily-energy"] = energy["summary"]
    (args.output/"measurements.json").write_text(
        json.dumps(measurements, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print(json.dumps({k: v.get("metrics", v) for k, v in measurements.items()}, indent=2))

if __name__ == "__main__":
    main()
