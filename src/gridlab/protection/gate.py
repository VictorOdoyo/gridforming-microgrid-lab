"""Latched inverter blocking with explicit reset and a healthy-voltage dwell."""

from dataclasses import dataclass


@dataclass
class GateSupervisor:
    trip_voltage_v: float = 450
    restart_voltage_v: float = 650
    trip_temperature_c: float = 70
    restart_temperature_c: float = 55
    dwell_s: float = 0.01
    enabled: bool = True
    reason: str | None = None
    healthy_s: float = 0.0
    reset_requested: bool = False

    def __post_init__(self):
        if not 0 < self.trip_voltage_v < self.restart_voltage_v or self.dwell_s < 0:
            raise ValueError("invalid voltage hysteresis or dwell")
        if self.restart_temperature_c >= self.trip_temperature_c:
            raise ValueError("invalid thermal hysteresis")

    def step(self, voltage_v, temperature_c, dt, reset=False):
        if dt <= 0:
            raise ValueError("positive sample interval required")
        self.reset_requested |= reset
        if voltage_v <= self.trip_voltage_v or temperature_c >= self.trip_temperature_c:
            self.enabled = False
            self.reason = "undervoltage" if voltage_v <= self.trip_voltage_v else "overtemperature"
        healthy = voltage_v >= self.restart_voltage_v and temperature_c <= self.restart_temperature_c
        self.healthy_s = self.healthy_s + dt if healthy else 0.0
        if not self.enabled and self.reset_requested and self.healthy_s >= self.dwell_s:
            self.enabled, self.reason, self.reset_requested = True, None, False
        return self.enabled
