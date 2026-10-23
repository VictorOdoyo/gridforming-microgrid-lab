"""A sampled phase-increment meter for nominal-frame phasors."""

from dataclasses import dataclass

import numpy as np

from gridlab.phasors import wrap_angle


@dataclass
class FrequencyMeter:
    nominal_hz: float = 50
    minimum_voltage: float = 0.1
    previous: complex | None = None

    def step(self, voltage, dt):
        if dt <= 0:
            raise ValueError("positive sample interval required")
        if abs(voltage) < self.minimum_voltage:
            self.previous = None
            return None
        previous = self.previous
        self.previous = voltage
        if previous is None:
            return None
        phase = wrap_angle(np.angle(voltage) - np.angle(previous))
        return float(self.nominal_hz + phase / (2 * np.pi * dt))
