"""Serializable real-valued signals evaluated at explicit control boundaries."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Signal:
    times: tuple
    values: tuple
    interpolation: str = "step"

    def __post_init__(self):
        if not self.times or len(self.times) != len(self.values) or self.times[0] != 0:
            raise ValueError("matching nonempty signal arrays starting at zero required")
        if np.any(np.diff(self.times) <= 0) or not np.all(np.isfinite([*self.times, *self.values])):
            raise ValueError("finite increasing signal times required")
        if self.interpolation not in ("step", "linear"):
            raise ValueError("unsupported signal interpolation")

    def __call__(self, time):
        if self.interpolation == "linear":
            return np.interp(time, self.times, self.values)
        index = np.clip(np.searchsorted(self.times, time, side="right") - 1, 0, len(self.values) - 1)
        return np.asarray(self.values)[index]
