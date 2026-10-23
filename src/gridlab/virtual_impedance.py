"""Fundamental-frequency virtual impedance as a voltage-reference correction."""
from dataclasses import dataclass

@dataclass(frozen=True)
class VirtualImpedance:
    resistance: float
    reactance: float

    def __post_init__(self):
        if self.resistance < 0 or self.reactance < 0:
            raise ValueError("virtual impedance must be passive")

    def compensate(self, reference, current):
        return reference-(self.resistance+1j*self.reactance)*current

    def adaptive(self, current_magnitude, threshold, gain):
        if threshold <= 0 or gain < 0:
            raise ValueError("invalid adaptive settings")
        return VirtualImpedance(self.resistance+gain*max(0, current_magnitude-threshold),
                                self.reactance)
