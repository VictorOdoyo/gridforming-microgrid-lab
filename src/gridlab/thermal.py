"""Lumped RC thermal model and explicitly empirical inverter loss curve."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ThermalRC:
    resistance_k_w: float
    capacity_j_k: float

    def __post_init__(self):
        if min(self.resistance_k_w, self.capacity_j_k) <= 0:
            raise ValueError("thermal R and C must be positive")

    def step(self, temperature_c, ambient_c, loss_w, dt):
        if dt < 0 or loss_w < 0:
            raise ValueError("invalid time or dissipation")
        target = ambient_c + loss_w * self.resistance_k_w
        decay = math.exp(-dt / (self.resistance_k_w * self.capacity_j_k))
        return target + (temperature_c - target) * decay


def converter_loss(
    current_rms_a,
    dc_voltage,
    switching_hz,
    resistance_ohm=0.01,
    switching_energy_j=0.001,
    reference_voltage=600.0,
    idle_w=10.0,
):
    if (
        min(current_rms_a, dc_voltage, switching_hz, resistance_ohm, switching_energy_j, idle_w) < 0
        or reference_voltage <= 0
    ):
        raise ValueError("loss model parameters must be nonnegative")
    return (
        idle_w
        + 3 * resistance_ohm * current_rms_a**2
        + 6 * switching_energy_j * switching_hz * dc_voltage / reference_voltage
    )
