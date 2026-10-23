"""Reduced diesel power actuator for dispatch and frequency studies."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class DieselGovernor:
    rated_kw: float
    tau_s: float = 0.5
    ramp_kw_s: float = 20.0
    min_kw: float = 0.0

    def __post_init__(self):
        if min(self.rated_kw, self.tau_s, self.ramp_kw_s) <= 0 or not 0 <= self.min_kw < self.rated_kw:
            raise ValueError("invalid governor parameters")

    def derivative(self, power_kw, request_kw, enabled=True):
        target = np.clip(request_kw, self.min_kw, self.rated_kw) if enabled else 0.0
        return float(np.clip((target - power_kw) / self.tau_s, -self.ramp_kw_s, self.ramp_kw_s))
