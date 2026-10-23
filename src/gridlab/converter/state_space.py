"""Analytical LC state-space matrices, avoiding numerical differentiation."""

import numpy as np


def lc_state_space(plant, conductance):
    if conductance < 0:
        raise ValueError("nonnegative conductance required")
    inductance, c, r, w = plant.inductance_h, plant.capacitance_f, plant.resistance_ohm, plant.omega
    a = np.array(
        [
            [-r / inductance, w, -1 / inductance, 0],
            [-w, -r / inductance, 0, -1 / inductance],
            [1 / c, 0, -conductance / c, w],
            [0, 1 / c, -w, -conductance / c],
        ]
    )
    b = np.array([[1 / inductance, 0], [0, 1 / inductance], [0, 0], [0, 0]])
    return a, b


def steady_state(plant, command_dq, conductance):
    a, b = lc_state_space(plant, conductance)
    return -np.linalg.solve(a, b @ np.array([command_dq.real, command_dq.imag]))
