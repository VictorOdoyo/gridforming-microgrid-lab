"""Exact zero-order-hold discretization via an augmented matrix exponential."""

import numpy as np
from scipy.linalg import expm


def zero_order_hold(a, b, dt):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or b.ndim != 2 or b.shape[0] != len(a) or dt <= 0:
        raise ValueError("invalid state-space dimensions or sample interval")
    n, m = b.shape
    augmented = np.zeros((n + m, n + m))
    augmented[:n, :n], augmented[:n, n:] = a, b
    transition = expm(augmented * dt)
    return transition[:n, :n], transition[:n, n:]


def schur_stable(matrix, margin=0.0):
    if not 0 <= margin < 1:
        raise ValueError("margin must lie in [0,1)")
    return bool(np.max(abs(np.linalg.eigvals(matrix))) < 1 - margin)
