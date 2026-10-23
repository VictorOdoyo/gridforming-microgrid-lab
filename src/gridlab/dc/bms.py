"""Sampled BMS supervisor; reset requires a healthy recovery band."""

from dataclasses import dataclass


@dataclass
class BMS:
    minimum_soc: float = 0.1
    recovery_soc: float = 0.15
    trip_temperature_c: float = 60
    reset_temperature_c: float = 50
    closed: bool = True
    reason: str | None = None

    def __post_init__(self):
        if not 0 <= self.minimum_soc < self.recovery_soc <= 1:
            raise ValueError("invalid SOC hysteresis")
        if self.reset_temperature_c >= self.trip_temperature_c:
            raise ValueError("temperature reset must be below trip")

    def step(self, soc, temperature_c, reset=False):
        if soc <= self.minimum_soc:
            self.closed, self.reason = False, "low-soc"
        elif temperature_c >= self.trip_temperature_c:
            self.closed, self.reason = False, "overtemperature"
        elif reset and soc >= self.recovery_soc and temperature_c <= self.reset_temperature_c:
            self.closed, self.reason = True, None
        return self.closed
