"""Continuous capacitor energy state with explicit brownout margin."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Bus:
    capacitance_f: float = 0.05
    nominal_v: float = 700
    minimum_v: float = 450

    def __post_init__(self):
        if not all(math.isfinite(v) for v in (self.capacitance_f, self.nominal_v, self.minimum_v)):
            raise ValueError("finite DC bus parameters required")
        if self.capacitance_f <= 0 or not 0 < self.minimum_v < self.nominal_v:
            raise ValueError("invalid DC bus ratings")

    def energy(self, voltage_v):
        if voltage_v < 0:
            raise ValueError("negative capacitor voltage")
        return 0.5 * self.capacitance_f * voltage_v**2

    def voltage(self, energy_j):
        if energy_j < 0:
            raise ValueError("negative DC stored energy")
        return math.sqrt(2 * energy_j / self.capacitance_f)

    def derivative(self, input_w, output_w):
        return input_w - output_w

    def time_to_brownout(self, energy_j, deficit_w):
        if deficit_w <= 0:
            return float("inf")
        return max(0, energy_j - self.energy(self.minimum_v)) / deficit_w
