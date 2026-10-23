"""Exact zero-order-held low-pass measurement updates."""

import math
from dataclasses import dataclass


@dataclass
class LowPass:
    tau: float
    value: float = 0.0

    def __post_init__(self):
        if not math.isfinite(self.tau) or self.tau <= 0:
            raise ValueError("tau must be positive")

    def step(self, measurement, dt):
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("dt must be nonnegative")
        self.value += -math.expm1(-dt / self.tau) * (measurement - self.value)
        return self.value


def filter_series(samples, dt, tau, initial=0.0):
    filt = LowPass(tau, initial)
    return [filt.step(x, dt) for x in samples]
