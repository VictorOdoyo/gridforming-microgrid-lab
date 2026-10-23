"""Static scientific figures with physical units and event annotations."""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
from matplotlib import pyplot as plt


def plot_result(result, path, title="Microgrid response", events=()):
    fig, axes = plt.subplots(4, 1, figsize=(11, 10), sharex=True, layout="constrained")
    for i, name in enumerate(result.source_names):
        frequency = np.where(result.enabled[:, i], result.frequency_hz[:, i], np.nan)
        axes[0].plot(result.time, frequency, label=name)
        axes[2].plot(result.time, result.power[:, i].real, label=name)
        axes[3].plot(result.time, abs(result.current[:, i]), label=name)
    for bus in range(result.voltage.shape[1]):
        axes[1].plot(result.time, abs(result.voltage[:, bus]), label=f"bus {bus}")
    axes[0].axhline(result.nominal_hz, color=".5", ls=":", lw=1)
    for ax, label in zip(
        axes,
        (
            "Internal frequency [Hz]",
            "Bus RMS voltage [pu]",
            "Terminal active power [pu]",
            "Source RMS current [pu]",
        ),
    ):
        ax.set_ylabel(label)
        ax.grid(alpha=0.2)
        ax.legend(loc="best", fontsize=8)
        for time in sorted({event.time for event in events}):
            ax.axvline(time, color=".4", ls="--", lw=0.8)
    axes[-1].set_xlabel("Time [s]")
    fig.suptitle(title, fontsize=14)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
