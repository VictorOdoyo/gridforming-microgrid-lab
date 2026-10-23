"""Deterministic profiles evaluated without mutable integration state."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Profile:
    times: tuple
    values: tuple

    def __post_init__(self):
        if len(self.times) != len(self.values) or not self.times:
            raise ValueError("equal nonempty arrays required")
        if not np.all(np.isfinite(self.times)) or not np.all(np.isfinite(self.values)):
            raise ValueError("profile values must be finite")
        if np.any(np.diff(self.times) <= 0):
            raise ValueError("times must strictly increase")

    def __call__(self, time):
        return np.interp(time, self.times, self.values)

def ramp(time, start, duration, initial=0.0, final=1.0):
    if duration <= 0:
        raise ValueError("ramp duration must be positive")
    return initial + (final-initial)*np.clip((np.asarray(time)-start)/duration, 0, 1)
