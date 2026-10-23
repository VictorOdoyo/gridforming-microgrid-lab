"""Three-phase bases: total VA, line-line RMS volts, and phase-current RMS amps."""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Base:
    power_va: float = 100_000.0
    voltage_ll_v: float = 400.0
    frequency_hz: float = 50.0

    def __post_init__(self):
        if not all(math.isfinite(x) and x > 0 for x in
                   (self.power_va, self.voltage_ll_v, self.frequency_hz)):
            raise ValueError("bases must be finite and positive")

    @property
    def current_a(self):
        return self.power_va / (math.sqrt(3) * self.voltage_ll_v)

    @property
    def impedance_ohm(self):
        return self.voltage_ll_v**2 / self.power_va

    @property
    def omega(self):
        return 2 * math.pi * self.frequency_hz

    def power_pu(self, watts):
        return watts / self.power_va

    def impedance_pu(self, ohms):
        return ohms / self.impedance_ohm
