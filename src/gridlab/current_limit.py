"""dq current commands in a voltage-oriented reference frame."""

import numpy as np


def limit_current(d, q, maximum, priority="radial"):
    if maximum <= 0:
        raise ValueError("maximum must be positive")
    if priority == "radial":
        scale = min(1, maximum / max(np.hypot(d, q), 1e-30))
        return float(d * scale), float(q * scale)
    if priority == "active":
        d = float(np.clip(d, -maximum, maximum))
        qmax = np.sqrt(max(0, maximum**2 - d**2))
        return d, float(np.clip(q, -qmax, qmax))
    if priority == "reactive":
        q = float(np.clip(q, -maximum, maximum))
        dmax = np.sqrt(max(0, maximum**2 - q**2))
        return float(np.clip(d, -dmax, dmax)), q
    raise ValueError("unknown current priority")
