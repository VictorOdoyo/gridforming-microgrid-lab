"""Reduced swing equation: 2H/f0 * df/dt = Pset-P-(df-secondary)/mp."""

from dataclasses import dataclass


@dataclass(frozen=True)
class VSM:
    inertia_s: float = 2.0
    droop_hz: float = 1.0
    nominal_hz: float = 50.0

    def __post_init__(self):
        if min(self.inertia_s, self.droop_hz, self.nominal_hz) <= 0:
            raise ValueError("VSM parameters must be positive")

    def derivative(self, deviation_hz, power_pu, reference_pu, secondary_hz=0.0):
        mismatch = reference_pu - power_pu - (deviation_hz - secondary_hz) / self.droop_hz
        return self.nominal_hz * mismatch / (2 * self.inertia_s)
