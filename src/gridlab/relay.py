"""Definite-time protection; pickup must remain active continuously."""

from dataclasses import dataclass


@dataclass
class DefiniteTimeRelay:
    threshold: float
    delay_s: float
    direction: str = "below"
    elapsed: float = 0.0
    tripped: bool = False

    def __post_init__(self):
        if self.delay_s < 0 or self.direction not in ("below", "above"):
            raise ValueError("invalid relay settings")

    def step(self, value, dt):
        if dt <= 0:
            raise ValueError("dt must be positive")
        pickup = value < self.threshold if self.direction == "below" else value > self.threshold
        self.elapsed = self.elapsed + dt if pickup else 0.0
        self.tripped = self.tripped or (pickup and self.elapsed >= self.delay_s - 1e-12)
        return self.tripped

    def reset(self):
        self.elapsed, self.tripped = 0.0, False
