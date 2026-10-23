"""Shared solver-boundary validation."""

import numpy as np


def integration_options(duration, sample_s, rtol, atol, max_step):
    values = np.array([duration, sample_s, rtol, atol, max_step], float)
    if not np.all(np.isfinite(values)) or np.any(values <= 0):
        raise ValueError(
            "duration, sample interval, tolerances, and maximum step must be finite and positive"
        )
    if duration / sample_s > 2_000_000:
        raise ValueError("requested output exceeds two million samples; increase sample interval")
