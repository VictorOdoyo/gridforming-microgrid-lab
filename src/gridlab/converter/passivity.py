"""Linear dissipation identity for the three-phase LC energy storage function."""

import numpy as np

from .state_space import lc_state_space


def storage_matrix(plant):
    return 1.5 * np.diag([plant.inductance_h] * 2 + [plant.capacitance_f] * 2)


def dissipation_matrix(plant, conductance):
    a, _ = lc_state_space(plant, conductance)
    w = storage_matrix(plant)
    return -(a.T @ w + w @ a) / 2


def passive(plant, conductance, tolerance=1e-9):
    return bool(np.linalg.eigvalsh(dissipation_matrix(plant, conductance)).min() >= -tolerance)
