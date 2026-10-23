"""Algebraic radial current saturation; fundamental-frequency approximation."""
import numpy as np
from scipy.optimize import root
from .norton import solve_network, NetworkPoint

def solve_limited(ybus, buses, impedances, emf, limits, enabled=None, tolerance=1e-9):
    buses, z, e = np.asarray(buses, int), np.asarray(impedances, complex), np.asarray(emf, complex)
    limits = np.asarray(limits, float)
    if limits.shape != e.shape or np.any(limits <= 0) or np.any(np.isnan(limits)):
        raise ValueError("positive current limits required for each source")
    initial = solve_network(ybus, buses, z, e, enabled)
    if np.all(abs(initial.current) <= limits):
        return initial
    y = np.asarray(ybus, complex)
    n = len(y)
    on = np.ones(len(e), bool) if enabled is None else np.asarray(enabled, bool)
    def currents(v):
        raw = np.where(on, (e-v[buses])/z, 0j)
        return raw*np.minimum(1, limits/np.maximum(abs(raw), 1e-30))
    def residual(x):
        v = x[:n]+1j*x[n:]
        mismatch = y@v
        np.add.at(mismatch, buses, -currents(v))
        return np.r_[mismatch.real, mismatch.imag]
    v0 = initial.voltage
    solution = root(residual, np.r_[v0.real, v0.imag], tol=tolerance)
    err = float(np.max(abs(residual(solution.x))))
    if not solution.success or err > tolerance*10:
        raise RuntimeError(f"current-limited network did not converge; KCL={err:g}")
    v = solution.x[:n]+1j*solution.x[n:]
    i = currents(v)
    return NetworkPoint(v, i, v[buses]*np.conj(i), err)
