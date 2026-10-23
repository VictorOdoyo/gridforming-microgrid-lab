"""Fixed-step utilities for sampled controllers; callbacks must be pure."""

import numpy as np


def rk4(function, time, state, step):
    if step <= 0:
        raise ValueError("positive integration step required")
    x = np.asarray(state, float)
    a = np.asarray(function(time, x))
    b = np.asarray(function(time + step / 2, x + step * a / 2))
    c = np.asarray(function(time + step / 2, x + step * b / 2))
    d = np.asarray(function(time + step, x + step * c))
    return x + step * (a + 2 * b + 2 * c + d) / 6


def ticks(duration, period):
    if not np.isfinite(duration + period) or min(duration, period) <= 0:
        raise ValueError("positive finite horizon and period required")
    return np.unique(np.r_[np.arange(int(np.ceil(duration / period))) * period, duration])


def rk4_substeps(function, time, state, step, count):
    if not isinstance(count, int) or count < 1:
        raise ValueError("positive integer substep count required")
    x = np.array(state, float)
    for k in range(count):
        x = rk4(function, time + k * step / count, x, step / count)
    return x


def merge_boundaries(time, boundaries):
    t = np.asarray(boundaries, float)
    if t.ndim != 1 or not np.all(np.isfinite(t)) or np.any(t < time[0]) or np.any(t > time[-1]):
        raise ValueError("finite boundaries inside the simulation horizon required")
    return np.unique(np.r_[time, t])
