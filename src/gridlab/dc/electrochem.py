"""One-RC pack state equations in SI; positive current discharges the pack."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Polarization:
    resistance_ohm: float = 0.03
    capacitance_f: float = 1000

    def __post_init__(self):
        if not all(math.isfinite(v) for v in vars(self).values()):
            raise ValueError("finite electrical elements required")
        if min(self.resistance_ohm, self.capacitance_f) <= 0:
            raise ValueError("positive RC elements required")

    def derivative(self, polarization_v, current_a):
        return (current_a - polarization_v / self.resistance_ohm) / self.capacitance_f

    def stored_j(self, polarization_v):
        return 0.5 * self.capacitance_f * polarization_v**2


def soc_derivative(current_a, capacity_ah, charge_coulomb_efficiency=0.995):
    if capacity_ah <= 0 or not 0 < charge_coulomb_efficiency <= 1:
        raise ValueError("invalid capacity or coulomb efficiency")
    effective = current_a if current_a >= 0 else current_a * charge_coulomb_efficiency
    return -effective / (capacity_ah * 3600)
