"""Local sampled closed-loop map around an unsaturated LC equilibrium."""

import numpy as np

from gridlab.discrete import zero_order_hold
from gridlab.linearize import jacobian

from .control import Cascade
from .lqr import voltage_equilibrium
from .state_space import lc_state_space


def sampled_cascade(plant, conductance=0.1, period_s=0.00005, delay_samples=0):
    if not isinstance(delay_samples, int) or delay_samples < 0:
        raise ValueError("nonnegative integer delay required")
    a, b = lc_state_space(plant, conductance)
    ad, bd = zero_order_hold(a, b, period_s)
    x, u = voltage_equilibrium(plant, conductance, 325 + 0j)
    current = complex(*x[:2])
    initial = np.r_[
        x,
        0,
        0,
        (plant.resistance_ohm * current).real,
        (plant.resistance_ohm * current).imag,
        np.tile([u.real, u.imag], delay_samples),
    ]

    def step(state):
        controller = Cascade.tuned(plant)
        controller.voltage_pi.integral = complex(*state[4:6])
        controller.current_pi.integral = complex(*state[6:8])
        command = controller.step(plant, state[:4], 325, 700, conductance, period_s)
        applied = complex(*state[8:10]) if delay_samples else command
        physical = ad @ state[:4] + bd @ [applied.real, applied.imag]
        integrals = [
            controller.voltage_pi.integral.real,
            controller.voltage_pi.integral.imag,
            controller.current_pi.integral.real,
            controller.current_pi.integral.imag,
        ]
        queue = np.r_[state[10:], command.real, command.imag] if delay_samples else np.array([])
        return np.r_[physical, integrals, queue]

    matrix = jacobian(step, initial, relative_step=1e-6)
    poles = np.linalg.eigvals(matrix)
    return {
        "matrix": matrix,
        "poles": poles,
        "spectral_radius": float(max(abs(poles))),
        "fixed_point_residual": float(max(abs(step(initial) - initial))),
    }
