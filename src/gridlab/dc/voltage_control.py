"""Sampled outer DC-voltage PI; output is battery-side current in amps."""

from dataclasses import dataclass, field

from gridlab.pi import PI


@dataclass
class DCVoltageControl:
    reference_v: float = 700
    kp_a_v: float = 2
    ki_a_vs: float = 20
    discharge_limit_a: float = 200
    charge_limit_a: float = 100
    pi: PI = field(init=False)

    def __post_init__(self):
        if min(self.reference_v, self.discharge_limit_a, self.charge_limit_a) <= 0:
            raise ValueError("positive ratings required")
        self.pi = PI(self.kp_a_v, self.ki_a_vs, -self.charge_limit_a, self.discharge_limit_a)

    def step(self, link_v, battery_v, requested_output_w, dt):
        if battery_v <= 0:
            raise ValueError("positive battery voltage required")
        feedforward = requested_output_w / battery_v
        return self.pi.step(self.reference_v - link_v, dt, feedforward)
