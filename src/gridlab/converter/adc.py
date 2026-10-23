"""Bipolar uniform ADC including both full-scale endpoints."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ADC:
    bits: int
    full_scale: float

    def __post_init__(self):
        if not isinstance(self.bits, int) or not 2 <= self.bits <= 24 or self.full_scale <= 0:
            raise ValueError("2 to 24 bits and positive full scale required")

    @property
    def lsb(self):
        return 2 * self.full_scale / (2**self.bits - 1)

    def encode(self, value):
        return np.rint(
            (np.clip(value, -self.full_scale, self.full_scale) + self.full_scale) / self.lsb
        ).astype(int)

    def decode(self, code):
        c = np.asarray(code)
        if np.any(c < 0) or np.any(c > 2**self.bits - 1):
            raise ValueError("code outside ADC range")
        return c * self.lsb - self.full_scale

    def measure(self, value):
        return self.decode(self.encode(value))
