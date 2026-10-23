"""Engineering PV availability model, not a switching or semiconductor solver."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class PVArray:
    rated_kw: float
    temperature_coefficient: float = -.004
    noct_c: float = 45.0
    inverter_efficiency: float = .97

    def __post_init__(self):
        if self.rated_kw <= 0 or not 0 < self.inverter_efficiency <= 1:
            raise ValueError("invalid PV rating or efficiency")

    def available_kw(self, irradiance_wm2, ambient_c=25.0):
        g = np.maximum(0, np.asarray(irradiance_wm2))
        cell = np.asarray(ambient_c)+(self.noct_c-20)*g/800
        thermal = np.maximum(0, 1+self.temperature_coefficient*(cell-25))
        return self.rated_kw*(g/1000)*thermal*self.inverter_efficiency

    def dispatch_kw(self, irradiance_wm2, ambient_c=25.0, limit_kw=None):
        available = self.available_kw(irradiance_wm2, ambient_c)
        return available if limit_kw is None else np.minimum(available, max(0, limit_kw))
