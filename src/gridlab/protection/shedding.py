"""Threshold-based staged disconnection; the caller selects Hz or pu voltage."""

from dataclasses import dataclass, field

import numpy as np


@dataclass
class StagedShedding:
    thresholds: tuple = (0.9, 0.8)
    fractions: tuple = (0.25, 0.25)
    delays_s: tuple = (0.02, 0.01)
    timers: np.ndarray = field(init=False)
    tripped: np.ndarray = field(init=False)

    def __post_init__(self):
        n = len(self.thresholds)
        if n == 0 or len(self.fractions) != n or len(self.delays_s) != n:
            raise ValueError("matching nonempty stages required")
        if min(self.fractions) <= 0 or sum(self.fractions) >= 1 or min(self.delays_s) < 0:
            raise ValueError("invalid stage fractions or delays")
        self.restore()

    def restore(self):
        self.timers = np.zeros(len(self.thresholds))
        self.tripped = np.zeros(len(self.thresholds), bool)

    def step(self, measurement, dt):
        if dt <= 0:
            raise ValueError("positive interval required")
        for k, threshold in enumerate(self.thresholds):
            pickup = measurement < threshold
            self.timers[k] = self.timers[k] + dt if pickup else 0
            self.tripped[k] |= pickup and self.timers[k] >= self.delays_s[k] - 1e-12
        return float(1 - np.dot(self.tripped, self.fractions))
