"""Sample-based settling with a required final in-band hold interval."""

import numpy as np

from .metrics import series


def settling_time(time, values, target, tolerance, after=0.0, hold_s=0.0):
    t, y = series(time, values)
    if y.ndim != 1 or tolerance < 0 or hold_s < 0 or after < t[0] or after > t[-1]:
        raise ValueError("invalid settling-time inputs")
    valid = np.flatnonzero(t >= after)
    bad = valid[abs(y[valid] - target) > tolerance]
    first = valid[0] if not len(bad) else bad[-1] + 1
    if first >= len(t) or t[-1] - t[first] < hold_s:
        return None
    return float(t[first] - after)
