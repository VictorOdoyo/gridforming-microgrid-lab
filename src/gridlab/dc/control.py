"""Sampled control supervisor; mutated only at accepted control ticks."""

from dataclasses import dataclass, field

from .bms import BMS
from .current_control import DCCurrentControl
from .derating import Envelope
from .voltage_control import DCVoltageControl


@dataclass
class DCControl:
    voltage: DCVoltageControl = field(default_factory=DCVoltageControl)
    current: DCCurrentControl = field(default_factory=DCCurrentControl)
    bms: BMS = field(default_factory=BMS)
    envelope: Envelope = field(default_factory=Envelope)
    reference_a: float = 0.0
    precharging: bool = False
    rearm_pending: bool = False
    precharge_fraction: float = 0.98

    def step(self, system, state, demand_w, dt, reset=False):
        soc, _, measured_a, _, temperature = state
        self.rearm_pending |= reset
        link = system.bus.voltage(state[3])
        pack_voltage = float(system.pack.ocv(soc)) - state[1]
        ready = link >= self.precharge_fraction * pack_voltage
        healthy = soc >= self.bms.recovery_soc and temperature <= self.bms.reset_temperature_c
        if self.bms.closed and not ready:
            self.bms.closed, self.bms.reason = False, "precharge-required"
            self.rearm_pending = True
        on = self.bms.step(soc, temperature, self.rearm_pending and ready)
        self.precharging = not on and self.rearm_pending and healthy and not ready
        if on:
            self.rearm_pending = False
        if not on:
            self.reference_a = 0.0
            self.current.integral_v = 0.0
            return 0.0, False
        lower, upper = self.envelope.limits(soc, temperature)
        self.voltage.pi.lower, self.voltage.pi.upper = lower, upper
        obs = system.observe(state, 0)
        request = self.voltage.step(obs["voltage_v"], obs["battery_voltage_v"], demand_w, dt)
        self.reference_a = self.envelope.constrain(request, soc, temperature)
        duty = self.current.step(
            self.reference_a,
            measured_a,
            obs["battery_voltage_v"],
            obs["voltage_v"],
            system.converter.resistance_ohm,
            dt,
        )
        return duty, True
