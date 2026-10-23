"""Relative-angle small-signal analysis around a synchronous operating point."""

import numpy as np

from .dynamics import Dynamics
from .linearize import jacobian
from .modes import modes, spectral_abscissa
from .operating_point import operating_point


def stability_report(config):
    point = operating_point(config)
    model = Dynamics(config)
    dropped = {5 * k + 1 for k, inv in enumerate(config.inverters) if inv.mode == "droop"}
    if config.secondary_gain == 0:
        dropped.add(len(point.state) - 1)
    if not model.grid_connected:
        dropped.add(0)
    keep = np.array([k for k in range(len(point.state)) if k not in dropped])

    def reduced_dynamics(reduced):
        state = point.state.copy()
        state[keep] = reduced
        derivative = model(0, state)
        if not model.grid_connected:
            common = derivative[0]
            derivative[np.arange(model.n) * 5] -= common
        return derivative[keep]

    matrix = jacobian(reduced_dynamics, point.state[keep])
    return {
        "common_deviation_hz": point.common_deviation_hz,
        "operating_point_residual": point.residual,
        "state_indices": keep.tolist(),
        "spectral_abscissa": spectral_abscissa(matrix),
        "modes": modes(matrix),
        "matrix": matrix.tolist(),
    }
