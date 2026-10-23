"""Averaged dead-time voltage error, without semiconductor switching transients."""

import numpy as np

from gridlab.transforms import clarke


def deadtime_error(phase_currents_a, dc_voltage, deadtime_s, switching_hz):
    currents = np.asarray(phase_currents_a)
    if currents.shape != (3,) or min(dc_voltage, deadtime_s, switching_hz) < 0:
        raise ValueError("invalid dead-time model inputs")
    if deadtime_s * switching_hz >= 0.5:
        raise ValueError("dead time must be shorter than half the switching period")
    phase_error = -dc_voltage * deadtime_s * switching_hz * np.sign(currents)
    result = clarke(phase_error)
    return complex(result[0], result[1])


def compensate_deadtime(command, phase_currents_a, dc_voltage, deadtime_s, switching_hz):
    return command - deadtime_error(phase_currents_a, dc_voltage, deadtime_s, switching_hz)
