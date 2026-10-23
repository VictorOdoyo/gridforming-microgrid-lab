"""Analytical lossless common-frequency benchmark on a shared system power base."""

import numpy as np


def equilibrium(total_load, references, droop_hz, secondary_hz=0.0):
    refs, gains = np.asarray(references, float), np.asarray(droop_hz, float)
    if refs.ndim != 1 or refs.shape != gains.shape or np.any(gains <= 0) or not len(refs):
        raise ValueError("matching nonempty references and positive gains required")
    df = secondary_hz + (refs.sum() - total_load) / np.sum(1 / gains)
    power = refs + (secondary_hz - df) / gains
    return float(df), power


def rating_scaled_droop(ratings_pu, full_load_deviation_hz=1.0):
    ratings = np.asarray(ratings_pu, float)
    if np.any(ratings <= 0) or full_load_deviation_hz <= 0:
        raise ValueError("ratings and full-load deviation must be positive")
    return full_load_deviation_hz / ratings
