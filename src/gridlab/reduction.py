"""Schur-complement reduction for zero-current-injection eliminated buses."""

import numpy as np


def kron_reduce(ybus, retain):
    y = np.asarray(ybus, dtype=complex)
    keep = np.asarray(retain, dtype=int)
    if len(set(keep)) != len(keep) or np.any(keep < 0) or np.any(keep >= len(y)):
        raise ValueError("retained bus indices must be unique and valid")
    drop = np.array([i for i in range(len(y)) if i not in keep], dtype=int)
    aa = y[np.ix_(keep, keep)]
    if not len(drop):
        return aa.copy()
    ab, ba, bb = y[np.ix_(keep, drop)], y[np.ix_(drop, keep)], y[np.ix_(drop, drop)]
    return aa - ab @ np.linalg.solve(bb, ba)
