"""PI requests inductor voltage; duty inversion accounts for half-bridge polarity."""

from dataclasses import dataclass

import numpy as np


@dataclass
class DCCurrentControl:
    kp_ohm: float = 1.0
    ki_ohm_s: float = 20
    integral_v: float = 0.0

    def step(self, reference_a, measured_a, battery_v, link_v, resistance_ohm, dt):
        if link_v <= 0 or dt <= 0 or min(self.kp_ohm, self.ki_ohm_s, resistance_ohm) < 0:
            raise ValueError("invalid current-controller inputs")
        error = reference_a - measured_a
        candidate = self.integral_v + self.ki_ohm_s * error * dt
        desired = self.kp_ohm * error + candidate
        # Positive inductor voltage needs a lower link-connection duty.
        raw_duty = (battery_v - resistance_ohm * measured_a - desired) / link_v
        achievable = battery_v - resistance_ohm * measured_a - np.clip(raw_duty, 0, 1) * link_v
        if 0 <= raw_duty <= 1 or error * (desired - achievable) <= 0:
            self.integral_v = candidate
        return float(
            np.clip(
                (battery_v - resistance_ohm * measured_a - self.kp_ohm * error - self.integral_v) / link_v,
                0,
                1,
            )
        )
