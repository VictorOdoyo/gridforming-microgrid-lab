"""Bounded parameter robustness, not a statistical guarantee of field reliability."""

from dataclasses import replace

from .cases import load_step
from .events import Event, run_events
from .summary import summarize
from .sweep import run_sweep
from .uncertainty import latin_hypercube, percentiles


def robustness_study(count=12, seed=42):
    base = load_step("vsm").config
    parameters = latin_hypercube(
        {"load_factor": (1.1, 1.8), "inertia_s": (1, 3), "droop_hz": (0.8, 1.2)}, count, seed
    )

    def evaluate(load_factor, inertia_s, droop_hz):
        config = replace(
            base, inverters=tuple(replace(i, inertia_s=inertia_s, droop_hz=droop_hz) for i in base.inverters)
        )
        result = run_events(config, (Event(0.5, "load_scale", load_factor),), 2, sample_s=0.05, max_step=0.05)
        return summarize(result)

    trials = run_sweep(evaluate, parameters)
    successful = [t.result["nadir_hz"] for t in trials if t.error is None]
    return {
        "trials": trials,
        "seed": seed,
        "failed_trials": sum(t.error is not None for t in trials),
        "nadir_percentiles_hz": percentiles(successful) if successful else None,
    }
