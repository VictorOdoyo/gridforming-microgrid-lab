"""Piecewise dynamics with right-continuous event observations."""

from dataclasses import dataclass, replace
from itertools import pairwise

import numpy as np
from scipy.integrate import solve_ivp

from .dynamics import Dynamics
from .simulation import Result, observe
from .synchronization import SyncCheck
from .validation import integration_options


@dataclass(frozen=True)
class Event:
    time: float
    kind: str
    value: float
    target: int = 0

    def __post_init__(self):
        if not np.isfinite(self.time) or self.time < 0 or not np.isfinite(self.value):
            raise ValueError("event time and value must be finite; time must be nonnegative")
        if not isinstance(self.target, int) or self.target < 0:
            raise ValueError("event target must be nonnegative")


def run_events(
    config,
    events=(),
    duration=10.0,
    sample_s=0.02,
    initial=None,
    rtol=1e-7,
    atol=1e-9,
    max_step=0.02,
    method="RK45",
):
    integration_options(duration, sample_s, rtol, atol, max_step)
    events = sorted(events, key=lambda e: e.time)
    if any(e.time > duration for e in events):
        raise ValueError("events must fall inside the simulation")
    for e in events:
        if (
            e.kind not in ("load_scale", "source_enabled", "p_ref", "line_enabled", "grid_enabled")
            or e.target
            >= (
                config.nbus
                if e.kind == "load_scale"
                else len(config.lines)
                if e.kind == "line_enabled"
                else 1
                if e.kind == "grid_enabled"
                else len(config.inverters)
            )
            or (e.kind == "load_scale" and e.value < 0)
            or (e.kind in ("source_enabled", "line_enabled", "grid_enabled") and e.value not in (0, 1))
        ):
            raise ValueError("invalid event kind, target, or value")
    scales = np.ones(config.nbus)
    enabled = np.ones(len(config.inverters), bool)
    refs = [inv.p_ref for inv in config.inverters]
    line_on = [line.enabled for line in config.lines]
    grid_on = config.grid is not None and config.grid.initially_connected
    if any(e.kind == "grid_enabled" for e in events) and config.grid is None:
        raise ValueError("grid events require a grid connection")

    def apply(time):
        nonlocal grid_on
        for event in events:
            if event.time == time:
                if event.kind == "load_scale":
                    scales[event.target] = event.value
                elif event.kind == "source_enabled":
                    enabled[event.target] = bool(event.value)
                elif event.kind == "grid_enabled":
                    if event.value and not grid_on:
                        candidate = Dynamics(
                            replace(
                                config,
                                loads=tuple(np.asarray(config.loads) * scales),
                                inverters=tuple(
                                    replace(inv, p_ref=refs[k]) for k, inv in enumerate(config.inverters)
                                ),
                                lines=tuple(
                                    replace(line, enabled=line_on[k]) for k, line in enumerate(config.lines)
                                ),
                            ),
                            enabled=enabled,
                            grid_connected=False,
                        )
                        local = candidate.network(x).voltage[config.grid.bus]
                        freq = config.base.frequency_hz + np.mean(candidate.frequencies(x)[enabled])
                        if not SyncCheck().accepts(
                            local, config.grid.voltage, freq, config.base.frequency_hz
                        ):
                            raise RuntimeError(f"unsafe synchronization at t={time:g}s")
                    grid_on = bool(event.value)
                elif event.kind == "line_enabled":
                    line_on[event.target] = bool(event.value)
                elif event.kind == "p_ref":
                    refs[event.target] = event.value
        sources = tuple(replace(inv, p_ref=refs[k]) for k, inv in enumerate(config.inverters))
        return Dynamics(
            replace(
                config,
                loads=tuple(np.asarray(config.loads) * scales),
                inverters=sources,
                lines=tuple(replace(line, enabled=line_on[k]) for k, line in enumerate(config.lines)),
            ),
            enabled=enabled,
            grid_connected=grid_on,
        )

    cuts = np.unique([0.0, duration, *[e.time for e in events]])
    samples = np.unique(np.r_[np.arange(0, duration, sample_s), cuts])
    x = Dynamics(config).initial() if initial is None else np.asarray(initial, float)
    if x.shape != (5 * len(config.inverters) + 1,) or not np.all(np.isfinite(x)):
        raise ValueError("invalid initial state")
    chunks = []
    for left, right in pairwise(cuts):
        model = apply(left)
        sol = solve_ivp(
            model, (left, right), x, dense_output=True, method=method, rtol=rtol, atol=atol, max_step=max_step
        )
        if not sol.success:
            raise RuntimeError(sol.message)
        times = samples[(samples >= left) & (samples < right)]
        chunks.append(observe(model, times, sol.sol(times).T))
        x = sol.y[:, -1]
    chunks.append(observe(apply(duration), [duration], x[None, :]))
    return Result(
        *(
            np.concatenate([getattr(r, attr) for r in chunks], axis=0)
            for attr in ("time", "state", "voltage", "power", "frequency_hz")
        ),
        chunks[0].source_names,
        config.base.frequency_hz,
        np.concatenate([r.current for r in chunks]),
        np.concatenate([r.network_residual for r in chunks]),
        np.concatenate([r.enabled for r in chunks]),
        solver_options={"method": method, "rtol": rtol, "atol": atol,
                        "max_step_s": max_step, "sample_s": sample_s},
    )
