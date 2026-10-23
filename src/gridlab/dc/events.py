"""Discrete DC supervisor events, processed outside continuous plant callbacks."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class DCEvent:
    time: float
    kind: str
    value: float = 0.0

    def __post_init__(self):
        if self.kind not in ("demand_w", "trip", "reset") or self.time < 0:
            raise ValueError("unsupported DC event")
        if not math.isfinite(self.time) or not math.isfinite(self.value):
            raise ValueError("finite event time and value required")
