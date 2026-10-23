"""State: five DC states followed by four peak-dq LC states."""

from dataclasses import dataclass, field

import numpy as np

from gridlab.converter.lc import LCPlant
from gridlab.dc.conversion import dc_demand
from gridlab.dc.system import DCSystem
from gridlab.modulation import limit_vector

from .grid_forming import GridForming


@dataclass(frozen=True)
class HybridPlant:
    dc: DCSystem = field(default_factory=DCSystem)
    ac: LCPlant = field(default_factory=LCPlant)
    inverter_resistance_ohm: float = 0.01
    inverter_idle_w: float = 20
    outer: GridForming | None = None

    def __post_init__(self):
        if min(self.inverter_resistance_ohm, self.inverter_idle_w) < 0:
            raise ValueError("nonnegative inverter losses required")

    def initial(self, soc=0.5):
        physical = np.r_[self.dc.initial(soc), np.zeros(4)]
        return physical if self.outer is None else np.r_[physical, np.zeros(4)]

    def observe(self, state, duty, command, closed=True, gate=True, precharge=False):
        dc_state, ac_state = state[:5], state[5:9]
        voltage_dc = self.dc.bus.voltage(dc_state[3])
        effective = complex(limit_vector(command, voltage_dc / np.sqrt(3))) if gate else 0j
        current = complex(*ac_state[:2])
        ac_input = 1.5 * (effective * current.conjugate()).real
        dc_input, loss = (
            dc_demand(ac_input, abs(current) / np.sqrt(2), self.inverter_resistance_ohm, self.inverter_idle_w)
            if gate
            else (0.0, 0.0)
        )
        return {
            **self.dc.observe(dc_state, duty, closed, precharge),
            "command": effective,
            "ac_input_w": ac_input,
            "inverter_dc_w": dc_input,
            "inverter_loss_w": loss,
        }

    def derivative(
        self, time, state, duty, command, conductance, closed=True, gate=True, pv_w=0.0, precharge=False
    ):
        p = self.observe(state, duty, command, closed, gate, precharge)
        if not np.isfinite(pv_w) or pv_w < 0:
            raise ValueError("nonnegative finite solar power required")
        dc_derivative = self.dc.derivative(time, state[:5], duty, p["inverter_dc_w"], closed, precharge)
        dc_derivative[3] += pv_w
        physical = np.r_[
            dc_derivative,
            self.ac.derivative(state[5:9], p["command"], conductance),
        ]

        if self.outer is None:
            return physical
        power = 1.5 * conductance * np.dot(state[7:9], state[7:9])
        outer = (
            self.outer.derivative(state[9:13], power, self.ac.omega / (2 * np.pi)) if gate else np.zeros(4)
        )
        return np.r_[physical, outer]

    def stored_j(self, state):
        return (
            state[3]
            + self.dc.converter.stored_j(state[2])
            + self.dc.polarization.stored_j(state[1])
            + self.ac.stored_j(state[5:9])
        )
