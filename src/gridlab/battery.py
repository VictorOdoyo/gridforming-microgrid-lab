"""Energy-bucket battery model; AC power is positive on discharge."""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Battery:
    capacity_kwh: float
    max_discharge_kw: float
    max_charge_kw: float
    efficiency_charge: float = .95
    efficiency_discharge: float = .95
    soc_min: float = .1
    soc_max: float = .9

    def __post_init__(self):
        values = vars(self).values()
        if not all(math.isfinite(x) for x in values):
            raise ValueError("battery parameters must be finite")
        if min(self.capacity_kwh, self.max_discharge_kw, self.max_charge_kw) <= 0:
            raise ValueError("capacity and power ratings must be positive")
        if not 0 <= self.soc_min < self.soc_max <= 1:
            raise ValueError("invalid state-of-charge interval")
        if not 0 < self.efficiency_charge <= 1 or not 0 < self.efficiency_discharge <= 1:
            raise ValueError("efficiency must lie in (0, 1]")

    def step(self, soc, requested_kw, dt_s):
        if dt_s <= 0 or not math.isfinite(dt_s) or not self.soc_min <= soc <= self.soc_max:
            raise ValueError("invalid time step or state of charge")
        hours = dt_s/3600
        discharge = min(self.max_discharge_kw,
                        (soc-self.soc_min)*self.capacity_kwh*self.efficiency_discharge/hours)
        charge = min(self.max_charge_kw,
                     (self.soc_max-soc)*self.capacity_kwh/(self.efficiency_charge*hours))
        actual = max(-charge, min(discharge, requested_kw))
        stored_kw = -actual/self.efficiency_discharge if actual >= 0 else -actual*self.efficiency_charge
        return soc+stored_kw*hours/self.capacity_kwh, actual
