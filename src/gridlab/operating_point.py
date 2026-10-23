"""Steady synchronous operation; island angles may rotate at a common deviation."""

from dataclasses import dataclass

import numpy as np
from scipy.optimize import root

from .dynamics import Dynamics


@dataclass(frozen=True)
class OperatingPoint:
    state: np.ndarray
    common_deviation_hz: float
    residual: float


def operating_point(config, tolerance=1e-8):
    if config.startup_s:
        raise ValueError("use the post-startup configuration with startup_s=0")
    model = Dynamics(config)
    connected = model.grid_connected
    initial = model.initial()

    def residual(z):
        x = z if connected else z[:-1]
        dx = model(0, x)
        for k, inv in enumerate(config.inverters):
            if inv.mode == "droop":
                dx[5 * k + 1] = x[5 * k + 1]
        if config.secondary_gain == 0:
            dx[-1] = x[-1]
        if connected:
            return dx
        dx[:-1].reshape(model.n, 5)[:, 0] -= 2 * np.pi * z[-1]
        return np.r_[dx, x[0]]

    guess = initial if connected else np.r_[initial, np.mean(model.frequencies(initial))]
    solution = root(residual, guess, tol=tolerance)
    err = float(np.max(abs(residual(solution.x))))
    if not solution.success or err > tolerance * 10:
        raise RuntimeError(f"operating point failed; residual={err:g}")
    x = solution.x if connected else solution.x[:-1]
    if np.any(x[:-1].reshape(model.n, 5)[:, 2] <= 0):
        raise RuntimeError("nonphysical operating-point voltage")
    return OperatingPoint(x, 0.0 if connected else float(solution.x[-1]), err)
