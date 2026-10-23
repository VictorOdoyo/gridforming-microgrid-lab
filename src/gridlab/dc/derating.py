"""Soft operating envelopes inside hard BMS trip boundaries."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Envelope:
    discharge_a: float = 200
    charge_a: float = 100
    soc_min: float = 0.1
    soc_max: float = 0.9
    taper_width: float = 0.05
    temperature_soft_c: float = 45
    temperature_hard_c: float = 60

    def __post_init__(self):
        if not 0 <= self.soc_min < self.soc_max <= 1 or self.taper_width <= 0:
            raise ValueError("invalid SOC envelope")
        if self.temperature_hard_c <= self.temperature_soft_c or min(self.discharge_a, self.charge_a) <= 0:
            raise ValueError("invalid current or thermal envelope")

    def limits(self, soc, temperature_c):
        thermal = float(
            np.clip(
                (self.temperature_hard_c - temperature_c)
                / (self.temperature_hard_c - self.temperature_soft_c),
                0,
                1,
            )
        )
        discharge = np.clip((soc - self.soc_min) / self.taper_width, 0, 1) * self.discharge_a * thermal
        charge = np.clip((self.soc_max - soc) / self.taper_width, 0, 1) * self.charge_a * thermal
        return float(-charge), float(discharge)

    def constrain(self, requested_a, soc, temperature_c):
        lower, upper = self.limits(soc, temperature_c)
        return float(np.clip(requested_a, lower, upper))
