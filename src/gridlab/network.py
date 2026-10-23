"""Balanced passive network stamping on a common per-unit base."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Line:
    start: int
    end: int
    r: float
    x: float
    b: float = 0.0
    enabled: bool = True

    def __post_init__(self):
        if self.start == self.end or min(self.start, self.end) < 0:
            raise ValueError("line must join two distinct nonnegative buses")
        if not np.all(np.isfinite([self.r, self.x, self.b])) or self.r < 0 or abs(self.r+1j*self.x) == 0:
            raise ValueError("invalid passive line impedance")

    @property
    def impedance(self):
        return self.r + 1j*self.x

def admittance(nbus, lines, shunts=None):
    if nbus < 1:
        raise ValueError("nbus must be positive")
    y = np.zeros((nbus, nbus), dtype=complex)
    for line in lines:
        if max(line.start, line.end) >= nbus:
            raise ValueError("line bus out of range")
        if not line.enabled:
            continue
        i, j = line.start, line.end
        g = 1/line.impedance
        y[i, i] += g + .5j*line.b
        y[j, j] += g + .5j*line.b
        y[i, j] -= g
        y[j, i] -= g
    if shunts is not None:
        shunts = np.asarray(shunts, dtype=complex)
        if shunts.shape != (nbus,):
            raise ValueError("one shunt required per bus")
        y += np.diag(shunts)
    return y
