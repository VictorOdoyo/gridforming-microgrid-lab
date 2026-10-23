"""Standalone nonlinear load experiment; dynamic scenarios use impedance loads."""

import numpy as np
from scipy.optimize import root

from .norton import NetworkPoint, solve_network


def solve_zip(ybus, buses, impedances, emf, loads, tolerance=1e-9):
    y = np.asarray(ybus, complex)
    n = len(y)
    if len(loads) != n:
        raise ValueError("one ZIP load required per bus")
    b, z, e = np.asarray(buses, int), np.asarray(impedances, complex), np.asarray(emf, complex)
    linear = y + np.diag([np.conj(load.power) for load in loads])
    start = solve_network(linear, b, z, e).voltage

    def residual(x):
        v = x[:n] + 1j * x[n:]
        mismatch = y @ v + np.array([load.current(v[k]) for k, load in enumerate(loads)])
        np.add.at(mismatch, b, -(e - v[b]) / z)
        return np.r_[mismatch.real, mismatch.imag]

    sol = root(residual, np.r_[start.real, start.imag], tol=tolerance)
    err = float(np.max(abs(residual(sol.x))))
    if not sol.success or err > 10 * tolerance:
        raise RuntimeError(f"ZIP network failed; residual={err:g}")
    v = sol.x[:n] + 1j * sol.x[n:]
    i = (e - v[b]) / z
    return NetworkPoint(v, i, v[b] * np.conj(i), err)
