"""Trace-level engineering summaries with connection-aware frequency metrics."""
import numpy as np
from .quality import voltage_metrics

def summarize(result):
    f, on, t = result.frequency_hz, result.enabled, result.time
    active = f[on]
    if len(t) < 2 or not active.size:
        raise ValueError("energized trace with at least two samples required")
    adjacent = on[1:] & on[:-1]
    rates = np.diff(f, axis=0)/np.diff(t)[:, None]
    final_error = abs(f[-1, on[-1]]-result.nominal_hz)
    deviation = np.where(on, abs(f-result.nominal_hz), 0)
    return {"nadir_hz": float(active.min()), "zenith_hz": float(active.max()),
            "max_abs_rocof_hz_s": float(abs(rates[adjacent]).max()) if adjacent.any() else 0.0,
            "final_max_error_hz": float(final_error.max()) if final_error.size else None,
            "integrated_absolute_error_hz_s": float(np.trapezoid(deviation, t, axis=0).sum()),
            "maximum_source_current_pu": float(abs(result.current).max()),
            "maximum_network_residual": float(result.network_residual.max()),
            "duration_s": float(t[-1]-t[0]),
            **voltage_metrics(t, result.voltage)}
