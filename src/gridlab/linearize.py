"""Numerical small-signal differentiation at a declared operating point."""
import numpy as np

def jacobian(function, state, relative_step=1e-5):
    x = np.asarray(state, float)
    if x.ndim != 1 or not np.all(np.isfinite(x)) or relative_step <= 0:
        raise ValueError("finite state vector and positive difference step required")
    baseline = np.atleast_1d(function(x))
    matrix = np.empty((len(baseline), len(x)))
    for k in range(len(x)):
        h = relative_step*max(1.0, abs(x[k]))
        delta = np.zeros_like(x)
        delta[k] = h
        matrix[:, k] = (np.asarray(function(x+delta))-np.asarray(function(x-delta)))/(2*h)
    return matrix
