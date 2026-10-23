"""Continuous DC plant state: SOC, RC polarization V, inductor A, capacitor J, temperature C."""

from dataclasses import dataclass, field

import numpy as np

from .bidirectional import Bidirectional
from .bus import Bus
from .electrochem import Polarization, soc_derivative
from .pack import Pack


@dataclass(frozen=True)
class DCSystem:
    pack: Pack = field(default_factory=Pack)
    polarization: Polarization = field(default_factory=Polarization)
    converter: Bidirectional = field(default_factory=Bidirectional)
    bus: Bus = field(default_factory=Bus)
    ambient_c: float = 25
    thermal_resistance_k_w: float = 0.02
    thermal_capacity_j_k: float = 10000
    dump_resistance_ohm: float = 1.0

    def __post_init__(self):
        if not np.all(
            np.isfinite(
                [
                    self.ambient_c,
                    self.thermal_resistance_k_w,
                    self.thermal_capacity_j_k,
                    self.dump_resistance_ohm,
                ]
            )
        ):
            raise ValueError("finite thermal parameters required")
        if min(self.thermal_resistance_k_w, self.thermal_capacity_j_k, self.dump_resistance_ohm) <= 0:
            raise ValueError("positive thermal and dump elements required")

    def initial(self, soc=0.5, voltage=None, current_a=0.0):
        self.pack.ocv(soc)
        return np.array(
            [
                soc,
                0,
                current_a,
                self.bus.energy(self.bus.nominal_v if voltage is None else voltage),
                self.ambient_c,
            ]
        )

    def observe(self, state, duty, closed=True):
        soc, vp, current, energy, temperature = state
        voltage = self.bus.voltage(energy)
        ocv = float(self.pack.ocv(soc))
        resistance = float(self.pack.resistance(temperature))
        battery_i = current if closed else 0.0
        terminal = ocv - vp - resistance * battery_i
        chemical_w = ocv * battery_i
        rc_loss = vp**2 / self.polarization.resistance_ohm
        ohmic = resistance * battery_i**2
        converter_loss = (self.converter.resistance_ohm if closed else self.dump_resistance_ohm) * current**2
        return {
            "voltage_v": voltage,
            "battery_voltage_v": terminal,
            "chemical_w": chemical_w,
            "battery_current_a": battery_i,
            "bus_input_w": duty * current * voltage if closed else 0.0,
            "heat_w": rc_loss + ohmic + converter_loss,
        }

    def derivative(self, time, state, duty, demand_w, closed=True):
        _soc, vp, current, _energy, temperature = state
        p = self.observe(state, duty, closed)
        di = (
            self.converter.derivative(current, p["battery_voltage_v"], p["voltage_v"], duty)
            if closed
            else -self.dump_resistance_ohm * current / self.converter.inductance_h
        )
        cooling = (temperature - self.ambient_c) / self.thermal_resistance_k_w
        return np.array(
            [
                soc_derivative(p["battery_current_a"], self.pack.capacity_ah, 1.0),
                self.polarization.derivative(vp, p["battery_current_a"]),
                di,
                p["bus_input_w"] - demand_w,
                (p["heat_w"] - cooling) / self.thermal_capacity_j_k,
            ]
        )
