"""Scientific figures for physical-model traces."""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
from matplotlib import pyplot as plt


def plot_case(case, trace, path):
    panels = 3 if case.kind in ("dc", "converter") else 5
    fig, axes = plt.subplots(panels, 1, figsize=(11, 2.2 * panels), sharex=True, layout="constrained")
    t = trace.time
    if case.kind == "dc":
        axes[0].plot(t, np.sqrt(2 * trace.state[:, 3] / case.plant.bus.capacitance_f))
        axes[0].set_ylabel("DC link [V]")
        axes[1].plot(t, trace.state[:, 2], label="inductor current")
        axes[1].plot(t, trace.reference_a, label="current reference", ls="--")
        axes[1].set_ylabel("Battery current [A]")
        axes[1].legend(fontsize=8)
        axes[2].plot(t, trace.state[:, 0])
        axes[2].set_ylabel("Battery SOC")
    elif case.kind == "converter":
        axes[0].plot(t, np.hypot(trace.state[:, 2], trace.state[:, 3]) * np.sqrt(1.5))
        axes[0].plot(t, abs(trace.reference) * np.sqrt(1.5), ls="--")
        axes[0].set_ylabel("AC line RMS [V]")
        axes[1].plot(t, np.hypot(trace.state[:, 0], trace.state[:, 1]) / np.sqrt(2))
        axes[1].set_ylabel("Phase RMS [A]")
        axes[2].plot(t, abs(trace.command), label="command")
        axes[2].plot(t, trace.dc_voltage / np.sqrt(3), ls="--", label="modulation limit")
        axes[2].set_ylabel("dq peak [V]")
        axes[2].legend(fontsize=8)
    else:
        voltage = np.hypot(trace.state[:, 7], trace.state[:, 8])
        axes[0].plot(t, np.sqrt(2 * trace.state[:, 3] / case.plant.dc.bus.capacitance_f))
        axes[0].set_ylabel("DC link [V]")
        axes[1].plot(t, voltage * np.sqrt(1.5))
        axes[1].set_ylabel("AC line RMS [V]")
        axes[2].plot(t, trace.state[:, 2])
        axes[2].set_ylabel("Battery current [A]")
        axes[3].plot(t, 1.5 * trace.conductance * voltage**2 / 1000, label="AC load")
        axes[3].plot(t, trace.solar_w / 1000, label="solar")
        axes[3].set_ylabel("Power [kW]")
        axes[3].legend(fontsize=8)
        axes[4].plot(t, trace.gate.astype(int), label="AC gate")
        axes[4].plot(t, trace.closed.astype(int), ls="--", label="battery contactor")
        axes[4].set_ylabel("Enabled")
        axes[4].legend(fontsize=8)
    for ax in axes:
        ax.grid(alpha=0.2)
        for event in case.events:
            ax.axvline(event.time, color=".5", lw=0.7, ls=":")
    axes[-1].set_xlabel("Time [s]")
    fig.suptitle(case.description)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
