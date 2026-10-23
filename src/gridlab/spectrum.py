"""Standalone waveform analysis; phasor solver output is not a switching waveform."""

import numpy as np


def amplitude_spectrum(samples, sample_hz, window="hann"):
    x = np.asarray(samples, float)
    if x.ndim != 1 or len(x) < 4 or sample_hz <= 0 or not np.all(np.isfinite(x)):
        raise ValueError("finite waveform with at least four samples required")
    if window not in ("hann", "rectangular"):
        raise ValueError("unsupported window")
    w = np.hanning(len(x)) if window == "hann" else np.ones(len(x))
    amplitudes = 2 * abs(np.fft.rfft(x * w)) / w.sum()
    amplitudes[0] /= 2
    if len(x) % 2 == 0:
        amplitudes[-1] /= 2
    return np.fft.rfftfreq(len(x), 1 / sample_hz), amplitudes


def coherent_thd(samples, sample_hz, fundamental_hz, highest=40):
    _, amplitude = amplitude_spectrum(samples, sample_hz, "rectangular")
    bin_hz = sample_hz / len(samples)
    if fundamental_hz <= 0 or not np.isclose(fundamental_hz / bin_hz, round(fundamental_hz / bin_hz)):
        raise ValueError("THD requires an integer number of fundamental cycles")
    k = round(fundamental_hz / bin_hz)
    if k >= len(amplitude) or amplitude[k] <= 1e-12:
        raise ValueError("fundamental missing or above Nyquist")
    indices = [k * h for h in range(2, highest + 1) if k * h < len(amplitude)]
    return float(np.linalg.norm(amplitude[indices]) / amplitude[k])
