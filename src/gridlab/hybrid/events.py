"""Events for the energy-coupled sampled plant."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class HybridEvent:
    time: float
    kind: str
    value: float = 0.0

    def __post_init__(self):
        if self.kind not in ("conductance", "reference_v", "battery-trip", "battery-reset", "gate-reset"):
            raise ValueError("unsupported hybrid event")
        if not math.isfinite(self.time) or self.time < 0 or not math.isfinite(self.value):
            raise ValueError("finite nonnegative event time required")
        if self.kind in ("conductance", "reference_v") and self.value < 0:
            raise ValueError("nonnegative load or reference required")
