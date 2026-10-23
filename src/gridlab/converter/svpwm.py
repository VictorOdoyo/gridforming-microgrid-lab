"""Centered common-mode injection for a two-level three-phase bridge."""

import numpy as np

from gridlab.modulation import limit_vector
from gridlab.transforms import clarke, inverse_clarke


def duties(alpha_beta, dc_voltage):
    if dc_voltage <= 0:
        raise ValueError("positive DC voltage required")
    command = complex(limit_vector(alpha_beta, dc_voltage / np.sqrt(3)))
    phases = inverse_clarke([command.real, command.imag, 0])
    common = (phases.max() + phases.min()) / 2
    return np.clip(0.5 + (phases - common) / dc_voltage, 0, 1)


def reconstruct(duty, dc_voltage):
    d = np.asarray(duty, float)
    if d.shape != (3,) or np.any(d < 0) or np.any(d > 1) or dc_voltage <= 0:
        raise ValueError("three legal duties and positive DC voltage required")
    ab0 = clarke((d - 0.5) * dc_voltage)
    return complex(ab0[0], ab0[1])
