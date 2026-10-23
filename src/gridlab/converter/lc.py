"""State [id, iq, vd, vq]; amplitude-invariant dq peak convention."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class LCPlant:
    inductance_h: float = 0.002
    capacitance_f: float = 50e-6
    resistance_ohm: float = 0.1
    omega: float = 2 * np.pi * 50

    def __post_init__(self):
        if min(self.inductance_h, self.capacitance_f) <= 0 or self.resistance_ohm < 0:
            raise ValueError("invalid passive LC elements")

    def derivative(self, state, command_dq, load_conductance):
        if load_conductance < 0:
            raise ValueError("passive load conductance required")
        i = state[0] + 1j * state[1]
        v = state[2] + 1j * state[3]
        di = (command_dq - v - self.resistance_ohm * i) / self.inductance_h - 1j * self.omega * i
        dv = (i - load_conductance * v) / self.capacitance_f - 1j * self.omega * v
        return np.array([di.real, di.imag, dv.real, dv.imag])

    def stored_j(self, state):
        return 0.75 * (
            self.inductance_h * np.dot(state[:2], state[:2])
            + self.capacitance_f * np.dot(state[2:], state[2:])
        )
