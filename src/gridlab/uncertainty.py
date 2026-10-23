"""Stratified uncertainty sampling and finite-result percentile summaries."""
import numpy as np
from scipy.stats import qmc

def latin_hypercube(bounds, count, seed=42):
    if count <= 0 or not bounds:
        raise ValueError("positive count and nonempty bounds required")
    names = tuple(bounds)
    limits = np.array([bounds[k] for k in names], float)
    if limits.shape != (len(names), 2) or np.any(limits[:, 0] >= limits[:, 1]):
        raise ValueError("each bound requires finite increasing endpoints")
    if not np.all(np.isfinite(limits)):
        raise ValueError("finite bounds required")
    unit = qmc.LatinHypercube(len(names), seed=seed).random(count)
    values = qmc.scale(unit, limits[:, 0], limits[:, 1])
    return [dict(zip(names, row)) for row in values]

def percentiles(values, levels=(5, 50, 95)):
    x = np.asarray(values, float)
    if not x.size or not np.all(np.isfinite(x)):
        raise ValueError("finite nonempty results required; handle failed trials explicitly")
    return dict(zip(levels, np.percentile(x, levels)))
