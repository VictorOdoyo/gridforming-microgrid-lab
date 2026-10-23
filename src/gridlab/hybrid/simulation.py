"""Energy-coupled sampled average inverter; no algebraic unlimited DC source."""

from dataclasses import dataclass

import numpy as np

from gridlab.numerics import rk4, ticks
from gridlab.protection.gate import GateSupervisor

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
    solar_w: np.ndarray


def simulate_hybrid(
    plant=None,
    duration=0.3,
    period_s=0.00005,
    initial=None,
    reference=None,
    conductance=None,
    control=None,
    events=(),
    supervisor=None,
    solar=None,
):
    plant = plant or HybridPlant()
    control = control or HybridControl.tuned(plant)
    reference = reference or (lambda t: 325 * min(1, t / 0.02))
    conductance = conductance or (lambda t: 0.1 if t < 0.1 else 0.2)
    solar = solar or (lambda t: 0.0)
    time = ticks(duration, period_s)
    if any(e.time > duration for e in events):
        raise ValueError("hybrid event outside horizon")
    time = np.unique(np.r_[time, [e.time for e in events]])
    supervisor = supervisor or GateSupervisor()
    load_override, ref_override = None, None
    x = plant.initial() if initial is None else np.array(initial, float)
    rows = []
    for k, t in enumerate(time):
        dt = time[k + 1] - t if k + 1 < len(time) else period_s
        reset_battery, reset_gate = False, False
        for event in events:
            if event.time == t:
                if event.kind == "conductance":
                    load_override = event.value
                elif event.kind == "reference_v":
                    ref_override = event.value
                elif event.kind == "battery-trip":
                    control.dc.bms.closed, control.dc.bms.reason = False, "external-trip"
                elif event.kind == "battery-reset":
                    reset_battery = True
                elif event.kind == "gate-reset":
                    reset_gate = True
        pv = float(solar(t))
        g = float(conductance(t) if load_override is None else load_override)
        ref = complex(reference(t) if ref_override is None else ref_override)
        gate = supervisor.step(plant.dc.bus.voltage(x[3]), x[4], dt, reset_gate)
        duty, command, closed = control.step(plant, x, ref, g, dt, gate=gate, reset=reset_battery, pv_w=pv)
        rows.append((x.copy(), duty, command, closed, gate, g, ref, pv))
        if k + 1 < len(time):
            x = rk4(
                lambda now, state: plant.derivative(now, state, duty, command, g, closed, gate, pv), t, x, dt
            )
            if x[3] <= 0:
                raise RuntimeError("DC bus depleted; enable brownout protection or reduce load")
    columns = [np.array([r[j] for r in rows]) for j in range(8)]
    return HybridTrace(time, *columns)
