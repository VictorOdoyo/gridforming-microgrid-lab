"""Cascade control uses SI peak dq voltages and currents."""

from dataclasses import dataclass

from .tuning import tune_lc
from .vector_pi import VectorPI


@dataclass
class Cascade:
    voltage_pi: VectorPI
    current_pi: VectorPI
    maximum_current_a: float = 150
    current_reference: complex = 0j

    @classmethod
    def tuned(cls, plant, maximum_current_a=150):
        gains = tune_lc(plant)
        return cls(
            VectorPI(gains.voltage_kp, gains.voltage_ki, 500),
            VectorPI(gains.current_kp, gains.current_ki, 2000),
            maximum_current_a,
        )

    def step(self, plant, state, voltage_reference, dc_voltage, conductance, dt):
        i, v = complex(*state[:2]), complex(*state[2:])
        load_current = conductance * v
        cap_decoupling = 1j * plant.omega * plant.capacitance_f * v
        self.current_reference = self.voltage_pi.step(
            voltage_reference - v, load_current + cap_decoupling, self.maximum_current_a, dt
        )
        feedforward = v + 1j * plant.omega * plant.inductance_h * i
        return self.current_pi.step(self.current_reference - i, feedforward, dc_voltage / 3**0.5, dt)
