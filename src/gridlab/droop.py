"""Droop gains use Hz/pu and pu-voltage/pu-reactive-power."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Droop:
    mp_hz: float = 1.0
    nq: float = .05
    nominal_hz: float = 50.0

    def __post_init__(self):
        if self.mp_hz <= 0 or self.nq < 0 or self.nominal_hz <= 0:
            raise ValueError("invalid droop gains")

    def frequency(self, measured_p, reference_p=0.0, secondary_hz=0.0):
        return self.nominal_hz+self.mp_hz*(reference_p-measured_p)+secondary_hz

    def voltage(self, measured_q, reference_q=0.0, reference_v=1.0):
        return reference_v+self.nq*(reference_q-measured_q)
