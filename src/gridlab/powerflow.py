"""Small-network AC load flow with one fixed slack bus."""
from dataclasses import dataclass
import numpy as np
from scipy.optimize import root

@dataclass(frozen=True)
class PowerFlow:
    voltage: np.ndarray
    injection: np.ndarray
    mismatch: float

def solve_powerflow(ybus, demand, slack=0, slack_voltage=1+0j, tolerance=1e-9):
    y = np.asarray(ybus, complex)
    demand = np.asarray(demand, complex)
    n = len(y)
    if y.shape != (n, n) or demand.shape != (n,) or not 0 <= slack < n:
        raise ValueError("invalid load-flow dimensions")
    pq = np.array([i for i in range(n) if i != slack], int)
    def voltage(x):
        v = np.full(n, complex(slack_voltage))
        v[pq] = x[:len(pq)] + 1j*x[len(pq):]
        return v
    def residual(x):
        v = voltage(x)
        mismatch = (v*np.conj(y@v)+demand)[pq]
        return np.r_[mismatch.real, mismatch.imag]
    initial = np.r_[np.full(len(pq), complex(slack_voltage).real),
                    np.full(len(pq), complex(slack_voltage).imag)]
    if len(pq):
        sol = root(residual, initial, tol=tolerance)
        err = float(np.max(np.abs(residual(sol.x))))
        if not sol.success or err > tolerance*10:
            raise RuntimeError(f"load flow failed; mismatch={err:g}")
        v = voltage(sol.x)
    else:
        v, err = voltage(initial), 0.0
    return PowerFlow(v, v*np.conj(y@v), err)
