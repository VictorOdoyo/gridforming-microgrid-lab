"""Fixed-step DC simulation with held duty and boundary-only supervisor updates."""

from dataclasses import dataclass

import numpy as np

from gridlab.numerics import merge_boundaries, rk4_substeps, ticks

from .control import DCControl
from .system import DCSystem


@dataclass(frozen=True)
class DCTrace:
    time: np.ndarray
    state: np.ndarray
    duty: np.ndarray
    reference_a: np.ndarray
    closed: np.ndarray
    demand_w: np.ndarray
    termination: str = "completed"


def simulate_dc(
    system=None,
    demand=None,
    duration=0.5,
    period_s=0.0001,
    initial=None,
    control=None,
    events=(),
    boundaries=(),
    integration_substeps=1,
):
    system = system or DCSystem()
    control = control or DCControl()
    demand = demand or (lambda t: 50000.0)
    time = merge_boundaries(ticks(duration, period_s), boundaries)
    if any(e.time > duration for e in events):
        raise ValueError("DC event outside simulation horizon")
    time = np.unique(np.r_[time, [e.time for e in events]])
    override = None
    x = system.initial() if initial is None else np.array(initial, float)
    if x.shape != (5,) or not np.isfinite(x).all():
        raise ValueError("invalid DC initial state")
    states, duties, references, statuses, loads, saved_times = [], [], [], [], [], []
    termination = "completed"
    for k, t in enumerate(time):
        dt = time[k + 1] - t if k + 1 < len(time) else period_s
        reset = False
        for event in events:
            if event.time == t:
                if event.kind == "demand_w":
                    override = event.value
                elif event.kind == "trip":
                    control.bms.closed, control.bms.reason = False, "external-trip"
                elif event.kind == "reset":
                    reset = True
        load = float(demand(t) if override is None else override)
        duty, closed = control.step(system, x, load, dt, reset=reset)
        saved_times.append(t)
        states.append(x.copy())
        duties.append(duty)
        references.append(control.reference_a)
        statuses.append(closed)
        loads.append(load)
        if system.bus.voltage(x[3]) < system.bus.minimum_v:
            termination = "undervoltage"
            break
        if k + 1 < len(time):
            x = rk4_substeps(
                lambda now, state: system.derivative(now, state, duty, load, closed),
                t,
                x,
                dt,
                integration_substeps,
            )
            if x[3] < 0:
                raise RuntimeError("DC energy crossed zero; reduce the integration period")
    return DCTrace(
        np.array(saved_times),
        np.array(states),
        np.array(duties),
        np.array(references),
        np.array(statuses),
        np.array(loads),
        termination,
    )
