"""Per-unit balanced phasors: S = V conjugate(I), positive power is injection."""

import numpy as np


def wrap_angle(angle):
    return (np.asarray(angle) + np.pi) % (2 * np.pi) - np.pi


def polar(magnitude, angle):
    return np.asarray(magnitude) * np.exp(1j * np.asarray(angle))


def complex_power(voltage, current):
    return np.asarray(voltage) * np.conj(current)


def power_factor(power):
    p = np.asarray(power, dtype=complex)
    return np.divide(p.real, np.abs(p), out=np.zeros_like(p.real), where=np.abs(p) > 0)
