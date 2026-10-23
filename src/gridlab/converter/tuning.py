"""Continuous design gains; sampled closed-loop behavior still requires verification."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class LoopGains:
    current_kp: float
    current_ki: float
    voltage_kp: float
    voltage_ki: float


def tune_lc(plant, current_bandwidth_hz=1000, voltage_bandwidth_hz=50, damping=0.707):
    if min(current_bandwidth_hz, voltage_bandwidth_hz, damping) <= 0:
        raise ValueError("positive bandwidths and damping required")
    if current_bandwidth_hz < 5 * voltage_bandwidth_hz:
        raise ValueError("inner-loop bandwidth must be at least five times outer bandwidth")
    wi, wv = 2 * math.pi * current_bandwidth_hz, 2 * math.pi * voltage_bandwidth_hz
    return LoopGains(
        plant.inductance_h * wi,
        plant.resistance_ohm * wi,
        2 * damping * wv * plant.capacitance_f,
        wv**2 * plant.capacitance_f,
    )
