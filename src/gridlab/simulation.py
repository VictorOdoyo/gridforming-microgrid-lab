"""Adaptive integration with explicitly sampled output."""

from dataclasses import dataclass, field, replace

import numpy as np
from scipy.integrate import solve_ivp

from .dynamics import Dynamics
from .validation import integration_options


@dataclass(frozen=True)
class Result:
    time: np.ndarray
    state: np.ndarray
    voltage: np.ndarray
    power: np.ndarray
    frequency_hz: np.ndarray
    source_names: tuple
    nominal_hz: float
    current: np.ndarray
    network_residual: np.ndarray
    enabled: np.ndarray
    solver_options: dict = field(default_factory=dict)


def observe(model, time, states):
    points = [model.network(x) for x in states]
    frequency = np.array([model.frequencies(x) for x in states]) + model.config.base.frequency_hz
    return Result(
        np.array(time),
        np.array(states),
        np.array([p.voltage for p in points]),
        np.array([p.power for p in points]),
        frequency,
        tuple(i.name for i in model.config.inverters),
        model.config.base.frequency_hz,
        np.array([p.current for p in points]),
        np.array([p.residual for p in points]),
        np.tile(model.enabled, (len(time), 1)),
    )


def simulate(
    config, duration=10.0, sample_s=0.02, initial=None, rtol=1e-7, atol=1e-9, method="RK45", max_step=0.02
):
    integration_options(duration, sample_s, rtol, atol, max_step)
    model = Dynamics(config)
    x0 = model.initial() if initial is None else np.asarray(initial, float)
    if x0.shape != (5 * model.n + 1,) or not np.all(np.isfinite(x0)):
        raise ValueError("invalid initial state")
    time = np.unique(np.r_[np.arange(0, duration, sample_s), duration])
    solution = solve_ivp(
        model, (0, duration), x0, t_eval=time, rtol=rtol, atol=atol, method=method, max_step=max_step
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return replace(observe(model, solution.t, solution.y.T),
                   solver_options={"method": method, "rtol": rtol, "atol": atol,
                                   "max_step_s": max_step, "sample_s": sample_s})
