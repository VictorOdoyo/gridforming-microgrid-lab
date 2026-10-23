"""Energy-coupled sampled average inverter; no algebraic unlimited DC source."""

from dataclasses import dataclass

import numpy as np

from gridlab.numerics import rk4, ticks

from .control import HybridControl
from .plant import HybridPlant


@dataclass(frozen=True)
class HybridTrace:
    time: np.ndarray
    state: np.ndarray
    duty: np.ndarray
    command: np.ndarray
    closed: np.ndarray
    gate: np.ndarray
    conductance: np.ndarray
    reference: np.ndarray


def simulate_hybrid(
    plant=None, duration=0.3, period_s=0.00005, initial=None, reference=None, conductance=None, control=None
):
    plant = plant or HybridPlant()
    control = control or HybridControl.tuned(plant)
    reference = reference or (lambda t: 325 * min(1, t / 0.02))
    conductance = conductance or (lambda t: 0.1 if t < 0.1 else 0.2)
    time = ticks(duration, period_s)
    x = plant.initial() if initial is None else np.array(initial, float)
    rows = []
    for k, t in enumerate(time):
        dt = time[k + 1] - t if k + 1 < len(time) else period_s
        g, ref = float(conductance(t)), complex(reference(t))
        duty, command, closed = control.step(plant, x, ref, g, dt)
        rows.append((x.copy(), duty, command, closed, True, g, ref))
        if k + 1 < len(time):
            x = rk4(lambda now, state: plant.derivative(now, state, duty, command, g, closed), t, x, dt)
            if x[3] <= 0:
                raise RuntimeError("DC bus depleted; enable brownout protection or reduce load")
    columns = [np.array([r[j] for r in rows]) for j in range(7)]
    return HybridTrace(time, *columns)
