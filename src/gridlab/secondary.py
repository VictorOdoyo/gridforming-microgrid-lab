"""Secondary frequency integral; output is a shared additive droop bias in Hz."""

import numpy as np


def secondary_rate(frequency_deviations, bias_hz, gain, limit_hz, weights=None):
    if gain < 0 or limit_hz <= 0:
        raise ValueError("invalid secondary gain or limit")
    error = -float(np.average(frequency_deviations, weights=weights))
    rate = gain * error
    if (bias_hz >= limit_hz and rate > 0) or (bias_hz <= -limit_hz and rate < 0):
        return 0.0
    return rate


def consensus_rate(biases, frequencies, laplacian, gain, coupling):
    b, f, lap = np.asarray(biases), np.asarray(frequencies), np.asarray(laplacian)
    if lap.shape != (len(b), len(b)) or f.shape != b.shape:
        raise ValueError("consensus dimensions do not match")
    if not np.allclose(lap.sum(axis=1), 0):
        raise ValueError("Laplacian rows must sum to zero")
    return -gain * f - coupling * (lap @ b)
