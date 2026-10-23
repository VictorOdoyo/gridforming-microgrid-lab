"""Ideal RC precharge from a stiff DC supply."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Precharge:
    resistance_ohm: float = 100
    capacitance_f: float = 0.05
    close_fraction: float = 0.95
    timeout_s: float = 20

    def __post_init__(self):
        if (
            min(self.resistance_ohm, self.capacitance_f, self.timeout_s) <= 0
            or not 0 < self.close_fraction < 1
        ):
            raise ValueError("invalid precharge parameters")

    def voltage(self, time_s, supply_v, initial_v=0):
        if time_s < 0 or not 0 <= initial_v <= supply_v:
            raise ValueError("invalid precharge state")
        return supply_v - (supply_v - initial_v) * math.exp(
            -time_s / (self.resistance_ohm * self.capacitance_f)
        )

    def resistor_energy_j(self, time_s, supply_v, initial_v=0):
        decay = math.exp(-2 * time_s / (self.resistance_ohm * self.capacitance_f))
        return 0.5 * self.capacitance_f * (supply_v - initial_v) ** 2 * (1 - decay)

    def ready(self, time_s, supply_v, initial_v=0):
        if supply_v <= 0:
            return False
        if time_s > self.timeout_s:
            raise RuntimeError("precharge timeout")
        return self.voltage(time_s, supply_v, initial_v) >= self.close_fraction * supply_v
