"""Controlled experiment: change only the grid-forming control mode."""
from .cases import load_step
from .events import run_events
from .metrics import frequency_metrics

def compare_controls(duration=None, sample_s=.02):
    results = {}
    for mode in ("droop", "vsm"):
        case = load_step(mode)
        horizon = case.duration if duration is None else duration
        events = tuple(e for e in case.events if e.time <= horizon)
        trace = run_events(case.config, events, horizon, sample_s)
        mask = trace.time >= 2 if horizon > 2 else trace.time >= 0
        results[mode] = {"trace": trace,
                         "metrics": frequency_metrics(trace.time[mask],
                                                      trace.frequency_hz[mask],
                                                      trace.nominal_hz)}
    return results
