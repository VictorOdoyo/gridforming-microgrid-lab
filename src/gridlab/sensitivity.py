"""Central-difference scalar study sensitivities with explicit step control."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Sensitivity:
    derivative: float
    elasticity: float | None
    baseline: float


def sensitivity(function, parameter, relative_step=1e-3, absolute_step=1e-6):
    if relative_step <= 0 or absolute_step <= 0:
        raise ValueError("difference steps must be positive")
    h = max(abs(parameter) * relative_step, absolute_step)
    baseline = float(function(parameter))
    derivative = float((function(parameter + h) - function(parameter - h)) / (2 * h))
    if not all(math.isfinite(x) for x in (baseline, derivative)):
        raise ValueError("nonfinite study response")
    return Sensitivity(derivative, None if baseline == 0 else derivative * parameter / baseline, baseline)
