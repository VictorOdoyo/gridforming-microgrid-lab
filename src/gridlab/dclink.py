"""Capacitor energy update in joules; power balance avoids dividing by voltage."""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class DCLink:
    capacitance_f: float

    def __post_init__(self):
        if self.capacitance_f <= 0:
            raise ValueError("capacitance must be positive")

    def energy(self, voltage_v):
        if voltage_v < 0:
            raise ValueError("voltage must be nonnegative")
        return .5*self.capacitance_f*voltage_v**2

    def step(self, voltage_v, input_w, output_w, dt):
        if dt < 0:
            raise ValueError("dt must be nonnegative")
        energy = self.energy(voltage_v)+(input_w-output_w)*dt
        if energy < 0:
            raise RuntimeError("DC link depleted before end of step")
        return math.sqrt(2*energy/self.capacitance_f)
