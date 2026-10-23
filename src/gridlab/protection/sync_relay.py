"""Sampled synchronization qualification built on the existing phasor criteria."""

from dataclasses import dataclass, field

from gridlab.synchronization import SyncCheck


@dataclass
class SyncRelay:
    criteria: SyncCheck = field(default_factory=SyncCheck)
    dwell_s: float = 0.2
    elapsed_s: float = 0

    def __post_init__(self):
        if self.dwell_s < 0:
            raise ValueError("nonnegative synchronization dwell required")

    def step(self, local, grid, local_hz, grid_hz, dt):
        if dt <= 0:
            raise ValueError("positive sample interval required")
        acceptable = self.criteria.accepts(local, grid, local_hz, grid_hz)
        self.elapsed_s = self.elapsed_s + dt if acceptable else 0.0
        return acceptable and self.elapsed_s >= self.dwell_s - 1e-12
