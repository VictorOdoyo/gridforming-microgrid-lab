"""Transformer pi-equivalent with complex tap on the sending side."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Transformer:
    start: int
    end: int
    impedance: complex
    tap: float = 1.0
    shift_rad: float = 0.0

    def stamp(self, ybus):
        if self.tap <= 0 or abs(self.impedance) == 0 or self.start == self.end:
            raise ValueError("invalid transformer")
        y = np.array(ybus, complex, copy=True)
        a = self.tap*np.exp(1j*self.shift_rad)
        g = 1/self.impedance
        i, j = self.start, self.end
        y[i, i] += g/abs(a)**2
        y[i, j] -= g/np.conj(a)
        y[j, i] -= g/a
        y[j, j] += g
        return y
