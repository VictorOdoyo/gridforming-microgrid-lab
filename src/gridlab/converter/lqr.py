"""Continuous full-state LQR design; reference feedforward uses a physical LC equilibrium."""

import numpy as np
from scipy.linalg import solve_continuous_are

from .state_space import lc_state_space


def lqr_gain(plant, conductance, state_weights=(1, 1, 10, 10), control_weight=0.1):
    a, b = lc_state_space(plant, conductance)
    q = np.diag(state_weights)
    if np.any(np.asarray(state_weights) <= 0) or control_weight <= 0:
        raise ValueError("positive definite LQR weights required")
    r = np.eye(2) * control_weight
    p = solve_continuous_are(a, b, q, r)
    gain = np.linalg.solve(r, b.T @ p)
    return gain, p


def voltage_equilibrium(plant, conductance, voltage_dq):
    current = (conductance + 1j * plant.omega * plant.capacitance_f) * voltage_dq
    command = voltage_dq + (plant.resistance_ohm + 1j * plant.omega * plant.inductance_h) * current
    return np.array([current.real, current.imag, voltage_dq.real, voltage_dq.imag]), command
