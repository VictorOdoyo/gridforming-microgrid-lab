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
