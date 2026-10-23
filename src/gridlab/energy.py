"""Integrate per-unit power on the declared three-phase system base."""
import numpy as np
from .metrics import series

def energy_kwh(time, power_pu, base_va):
    if base_va <= 0:
        raise ValueError("base power must be positive")
    t, p = series(time, power_pu)
    return np.trapezoid(p, t, axis=0)*base_va/3_600_000

def source_losses(time, current_pu, impedances, base_va):
    current = np.asarray(current_pu)
    resistance = np.real(np.asarray(impedances))
    if current.ndim != 2 or current.shape[1] != len(resistance) or np.any(resistance < 0):
        raise ValueError("current columns and passive source impedances required")
    return energy_kwh(time, abs(current)**2*resistance, base_va)
