"""Compare trajectories sampled at matching times; do not compare array indices blindly."""

import numpy as np


def trajectory_error(reference, candidate, attribute="frequency_hz"):
    if candidate.time[0] < reference.time[0] or candidate.time[-1] > reference.time[-1]:
        raise ValueError("candidate must lie inside reference horizon")
    expected = np.asarray(getattr(reference, attribute))
    actual = np.asarray(getattr(candidate, attribute))
    if expected.ndim != 2 or actual.shape[1:] != expected.shape[1:]:
        raise ValueError("matching two-dimensional signals required")
    interpolated = np.column_stack(
        [np.interp(candidate.time, reference.time, expected[:, k]) for k in range(expected.shape[1])]
    )
    delta = abs(actual - interpolated)
    return {"max_abs": float(delta.max()), "rms": float(np.sqrt(np.mean(delta**2)))}


def observed_order(coarse_error, fine_error, refinement=2):
    if min(coarse_error, fine_error) <= 0 or refinement <= 1:
        raise ValueError("positive errors and refinement greater than one required")
    return float(np.log(coarse_error / fine_error) / np.log(refinement))
