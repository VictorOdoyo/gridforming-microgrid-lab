"""Positive P and Q denote consumption on the system base."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ZIPLoad:
    power: complex
    z: float = 1.0
    i: float = 0.0
    p: float = 0.0
    frequency_coefficient: float = 0.0

    def __post_init__(self):
        if min(self.z, self.i, self.p) < 0 or not np.isclose(self.z + self.i + self.p, 1):
            raise ValueError("ZIP fractions must be nonnegative and sum to one")
        if not np.isfinite(self.power):
            raise ValueError("power must be finite")

    def demand(self, voltage, frequency_pu=1.0):
        v = np.abs(voltage)
        scale = self.z * v * v + self.i * v + self.p
        frequency = np.maximum(0, 1 + self.frequency_coefficient * (np.asarray(frequency_pu) - 1))
        return self.power * scale * frequency

    def current(self, voltage, floor=0.1):
        if floor <= 0:
            raise ValueError("voltage floor must be positive")
        v = np.asarray(voltage, complex)
        # Fold back power smoothly below floor to avoid singular current.
        denominator = np.maximum(abs(v) ** 2, floor**2)
        return np.conj(self.demand(v)) * v / denominator
