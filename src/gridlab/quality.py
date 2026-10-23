"""Phasor quality metrics; waveform harmonic distortion is not inferred."""
import numpy as np
from .metrics import series

def voltage_metrics(time, voltage, lower=.9, upper=1.1):
    if not 0 <= lower < upper:
        raise ValueError("invalid voltage band")
    t, v = series(time, abs(np.asarray(voltage)))
    outside = (v < lower) | (v > upper)
    return {"minimum_pu": float(v.min()), "maximum_pu": float(v.max()),
            "outside_band_bus_seconds": float(np.sum(np.trapezoid(outside.astype(float), t, axis=0)))}

def sharing_error(power, ratings):
    p, r = np.asarray(power, float), np.asarray(ratings, float)
    if p.shape != r.shape or np.any(r <= 0):
        raise ValueError("matching powers and positive ratings required")
    normalized = p/r
    return float(np.max(abs(normalized-np.average(normalized, weights=r))))
