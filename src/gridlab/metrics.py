"""Metrics on sampled trajectories; RoCoF depends on output sampling."""

import numpy as np


def series(time, values):
    t, y = np.asarray(time, float), np.asarray(values, float)
    if t.ndim != 1 or len(t) < 2 or len(y) != len(t) or np.any(np.diff(t) <= 0):
        raise ValueError("strictly increasing time with at least two matching samples required")
    if not np.all(np.isfinite(t)) or not np.all(np.isfinite(y)):
        raise ValueError("finite time series required")
    return t, y


def frequency_metrics(time, frequency, nominal=50.0):
    t, f = series(time, frequency)
    deviation = f - nominal
    rocof = np.diff(f, axis=0) / np.diff(t).reshape((-1,) + (1,) * (f.ndim - 1))
    return {
        "nadir_hz": float(np.min(f)),
        "zenith_hz": float(np.max(f)),
        "max_abs_rocof_hz_s": float(np.max(abs(rocof))),
        "final_max_error_hz": float(np.max(abs(deviation[-1]))),
        "integrated_absolute_error_hz_s": float(np.sum(np.trapezoid(abs(deviation), t, axis=0))),
    }
