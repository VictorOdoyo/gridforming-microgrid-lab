"""Sampled PI regulator with conditional integration at output saturation."""

from dataclasses import dataclass

import numpy as np


@dataclass
class PI:
    kp: float
    ki: float
    lower: float = -float("inf")
    upper: float = float("inf")
    integral: float = 0.0

    def __post_init__(self):
        if min(self.kp, self.ki) < 0 or self.lower >= self.upper:
            raise ValueError("invalid PI gains or bounds")

    def step(self, error, dt, feedforward=0.0):
        if dt <= 0:
            raise ValueError("dt must be positive")
        candidate = self.integral + self.ki * error * dt
        raw = self.kp * error + candidate + feedforward
        if (
            self.lower <= raw <= self.upper
            or (raw > self.upper and error < 0)
            or (raw < self.lower and error > 0)
        ):
            self.integral = candidate
        return float(np.clip(self.kp * error + self.integral + feedforward, self.lower, self.upper))
