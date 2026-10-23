"""Outer frequency control state [angle, deviation Hz, filtered power pu, secondary Hz]."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class GridForming:
    mode: str = "vsm"
    power_base_w: float = 100000
    reference_pu: float = 0.3
    droop_hz: float = 1
    inertia_s: float = 2
    power_tau_s: float = 0.02
    secondary_gain: float = 0

    def __post_init__(self):
        if (
            self.mode not in ("droop", "vsm")
            or min(self.power_base_w, self.droop_hz, self.inertia_s, self.power_tau_s) <= 0
            or self.secondary_gain < 0
        ):
            raise ValueError("invalid grid-forming settings")

    def deviation(self, state):
        return float(
            state[1] if self.mode == "vsm" else self.droop_hz * (self.reference_pu - state[2]) + state[3]
        )

    def derivative(self, state, load_w, nominal_hz):
        _, df, power, bias = state
        frequency = self.deviation(state)
        swing = (
            (nominal_hz / (2 * self.inertia_s) * (self.reference_pu - power - (df - bias) / self.droop_hz))
            if self.mode == "vsm"
            else 0
        )
        return np.array(
            [
                2 * np.pi * frequency,
                swing,
                (load_w / self.power_base_w - power) / self.power_tau_s,
                -self.secondary_gain * frequency,
            ]
        )
