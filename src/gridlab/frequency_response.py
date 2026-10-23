"""Continuous-time state-space frequency response in radians per second."""

import numpy as np


def frequency_response(a, b, c, d, omega):
    a, b, c, d = [np.atleast_2d(np.asarray(x, float)) for x in (a, b, c, d)]
    if a.shape[0] != a.shape[1] or b.shape[0] != len(a) or c.shape[1] != len(a):
        raise ValueError("incompatible state-space matrices")
    if d.shape != (c.shape[0], b.shape[1]):
        raise ValueError("feedthrough dimensions do not match")
    w = np.atleast_1d(omega)
    if np.any(w < 0):
        raise ValueError("frequencies must be nonnegative")
    return np.array([c @ np.linalg.solve(1j * f * np.eye(len(a)) - a, b) + d for f in w])
