"""Exact integral of the piecewise-linear open-circuit voltage table."""

import numpy as np


def chemical_energy(pack, soc):
    if not 0 <= soc <= 1:
        raise ValueError("SOC outside [0,1]")
    points = [p for p in pack.soc_points if p < soc] + [soc]
    if len(points) < 2:
        return 0.0
    voltage = pack.ocv(points)
    return float(np.trapezoid(voltage, points) * pack.capacity_ah * 3600)


def chemical_capacity_kwh(pack):
    return chemical_energy(pack, 1) / 3_600_000
