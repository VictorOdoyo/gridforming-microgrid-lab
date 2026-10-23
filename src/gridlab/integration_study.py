"""Integrator convergence experiment with identical sample and event times."""
from .cases import load_step
from .events import run_events
from .convergence import trajectory_error

def integration_study(steps=(.1, .05, .02), duration=3):
    case = load_step("vsm")
    if duration <= 2:
        raise ValueError("duration must include post-disturbance response")
    reference = run_events(case.config, case.events, duration, sample_s=.02,
                           max_step=.005, rtol=1e-10, atol=1e-12)
    rows = []
    for step in steps:
        candidate = run_events(case.config, case.events, duration, sample_s=.02,
                               max_step=step, rtol=1e-5, atol=1e-7)
        rows.append({"max_step_s": step,
                     "frequency_error": trajectory_error(reference, candidate),
                     "state_error": trajectory_error(reference, candidate, "state")})
    return rows
