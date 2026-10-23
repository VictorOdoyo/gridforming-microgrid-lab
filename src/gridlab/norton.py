"""Linear network solve for voltage sources behind series impedances."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class NetworkPoint:
    voltage: np.ndarray
    current: np.ndarray
    power: np.ndarray
    residual: float


def solve_network(ybus, buses, impedances, emf, enabled=None):
    y = np.array(ybus, dtype=complex, copy=True)
    buses = np.asarray(buses, dtype=int)
    z = np.asarray(impedances, dtype=complex)
    e = np.asarray(emf, dtype=complex)
    if not (buses.shape == z.shape == e.shape) or buses.ndim != 1:
        raise ValueError("source arrays must be matching vectors")
    if y.ndim != 2 or y.shape[0] != y.shape[1] or np.any(buses < 0) or np.any(buses >= len(y)):
        raise ValueError("invalid network dimensions or source buses")
    if np.any(abs(z) == 0):
        raise ValueError("source impedances must be nonzero")
    on = np.ones(len(e), dtype=bool) if enabled is None else np.asarray(enabled, dtype=bool)
    if on.shape != e.shape:
        raise ValueError("source mask length mismatch")
    ys = np.where(on, 1 / z, 0)
    rhs = np.zeros(len(y), complex)
    np.add.at(y, (buses, buses), ys)
    np.add.at(rhs, buses, ys * e)
    try:
        v = np.linalg.solve(y, rhs)
    except np.linalg.LinAlgError as exc:
        raise ValueError("network is singular; check ungrounded islands") from exc
    current = ys * (e - v[buses])
    return NetworkPoint(v, current, v[buses] * np.conj(current), float(np.linalg.norm(y @ v - rhs, np.inf)))
