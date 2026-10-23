"""Ideal two-level bridge waveform synthesis; no device loss or gate-delay model."""

import numpy as np


def triangular_carrier(time, switching_hz):
    if switching_hz <= 0:
        raise ValueError("positive switching frequency required")
    phase = (np.asarray(time) * switching_hz) % 1
    return 1 - abs(2 * phase - 1)


def bridge_states(time, duty, switching_hz):
    d = np.asarray(duty)
    if d.shape != (3,) or np.any(d < 0) or np.any(d > 1):
        raise ValueError("three duties in [0,1] required")
    return (d[None, :] >= triangular_carrier(time, switching_hz)[:, None]).astype(int)


def phase_voltages(states, dc_voltage):
    s = np.asarray(states)
    if s.shape[-1] != 3 or not np.all((s == 0) | (s == 1)):
        raise ValueError("binary three-leg bridge states required")
    poles = dc_voltage * (s - 0.5)
    return poles - poles.mean(axis=-1, keepdims=True)
