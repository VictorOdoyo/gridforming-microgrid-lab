"""Stationary-frame LCL component model in SI units, one complex alpha-beta pair."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class LCLFilter:
    l1: float
    l2: float
    capacitance: float
    r1: float = 0.0
    r2: float = 0.0

    def __post_init__(self):
        if min(self.l1, self.l2, self.capacitance) <= 0 or min(self.r1, self.r2) < 0:
            raise ValueError("invalid LCL elements")

    @property
    def resonance_hz(self):
        return np.sqrt((self.l1 + self.l2) / (self.l1 * self.l2 * self.capacitance)) / (2 * np.pi)

    def derivative(self, state, converter_voltage, grid_voltage):
        i1, vc, i2 = state
        return np.array(
            [
                (converter_voltage - vc - self.r1 * i1) / self.l1,
                (i1 - i2) / self.capacitance,
                (vc - grid_voltage - self.r2 * i2) / self.l2,
            ],
            complex,
        )
