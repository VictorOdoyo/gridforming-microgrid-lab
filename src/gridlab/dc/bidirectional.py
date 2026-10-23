"""Averaged half-bridge converter; duty connects battery inductor to DC link."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Bidirectional:
    inductance_h: float = 0.005
    resistance_ohm: float = 0.05

    def __post_init__(self):
        if self.inductance_h <= 0 or self.resistance_ohm < 0:
            raise ValueError("invalid converter RL elements")

    def derivative(self, current_a, battery_v, link_v, duty):
        if not 0 <= duty <= 1:
            raise ValueError("duty outside [0,1]")
        return (battery_v - duty * link_v - self.resistance_ohm * current_a) / self.inductance_h

    def bus_current(self, current_a, duty):
        if not 0 <= duty <= 1:
            raise ValueError("duty outside [0,1]")
        return duty * current_a

    def stored_j(self, current_a):
        return 0.5 * self.inductance_h * current_a**2

    def loss_w(self, current_a):
        return self.resistance_ohm * current_a**2
