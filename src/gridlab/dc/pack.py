"""Pack-scale electrical parameters; tabulated OCV versus SOC."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Pack:
    capacity_ah: float = 200
    soc_points: tuple = (0, 0.1, 0.5, 0.9, 1)
    ocv_volts: tuple = (500, 560, 620, 665, 680)
    resistance_ohm: float = 0.08
    resistance_temp_coefficient: float = -0.005

    def __post_init__(self):
        if not np.all(np.isfinite([self.capacity_ah, self.resistance_ohm, self.resistance_temp_coefficient])):
            raise ValueError("finite pack parameters required")
        if min(self.ocv_volts) <= 0:
            raise ValueError("positive open-circuit voltages required")
        if self.capacity_ah <= 0 or self.resistance_ohm <= 0:
            raise ValueError("positive capacity and resistance required")
        if len(self.soc_points) != len(self.ocv_volts) or len(self.soc_points) < 2:
            raise ValueError("matching OCV table required")
        if self.soc_points[0] != 0 or self.soc_points[-1] != 1:
            raise ValueError("OCV table must cover SOC zero to one")
        if np.any(np.diff(self.soc_points) <= 0) or np.any(np.diff(self.ocv_volts) < 0):
            raise ValueError("OCV table must be monotonic")
        if not np.all(np.isfinite([*self.soc_points, *self.ocv_volts])):
            raise ValueError("finite table values required")

    def ocv(self, soc):
        if not np.all((np.asarray(soc) >= 0) & (np.asarray(soc) <= 1)):
            raise ValueError("SOC outside [0, 1]")
        return np.interp(soc, self.soc_points, self.ocv_volts)

    def resistance(self, temperature_c):
        return self.resistance_ohm * np.exp(
            self.resistance_temp_coefficient * (np.asarray(temperature_c) - 25)
        )
