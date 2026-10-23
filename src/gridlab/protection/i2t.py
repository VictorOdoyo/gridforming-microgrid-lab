"""Normalized excess-I-squared thermal stress; not a standard-specific relay curve."""

from dataclasses import dataclass


@dataclass
class I2T:
    pickup_a: float
    threshold_s: float
    cooling_tau_s: float = 10
    stress: float = 0.0
    tripped: bool = False

    def __post_init__(self):
        if min(self.pickup_a, self.threshold_s, self.cooling_tau_s) <= 0:
            raise ValueError("positive protection settings required")

    def step(self, current_a, dt):
        if dt <= 0:
            raise ValueError("positive time step required")
        excess = max(0, (abs(current_a) / self.pickup_a) ** 2 - 1)
        self.stress = max(0, self.stress + dt * (excess if excess else -self.stress / self.cooling_tau_s))
        self.tripped |= self.stress >= self.threshold_s - 1e-12
        return self.tripped

    def reset(self):
        self.stress, self.tripped = 0.0, False
