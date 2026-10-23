"""Single-RC terminal model using SI units and zero-order-held current."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class TheveninCell:
    r0: float
    r1: float
    c1: float
    ocv_empty: float = 3.0
    ocv_full: float = 4.2

    def __post_init__(self):
        if min(self.r0, self.r1, self.c1) <= 0:
            raise ValueError("resistance and capacitance must be positive")

    def step(self, polarization_v, current_a, soc, dt):
        if dt < 0 or not 0 <= soc <= 1:
            raise ValueError("invalid step or state of charge")
        decay = math.exp(-dt / (self.r1 * self.c1))
        vp = decay * polarization_v + self.r1 * current_a * (1 - decay)
        ocv = self.ocv_empty + soc * (self.ocv_full - self.ocv_empty)
        return vp, ocv - self.r0 * current_a - vp
