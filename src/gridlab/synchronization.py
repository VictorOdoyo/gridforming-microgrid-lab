"""Synchronization criteria evaluated on RMS bus phasors."""
from dataclasses import dataclass
import numpy as np
from .phasors import wrap_angle

@dataclass(frozen=True)
class SyncCheck:
    angle_rad: float = np.deg2rad(10)
    frequency_hz: float = .1
    voltage_pu: float = .1
    minimum_voltage: float = .5

    def __post_init__(self):
        if min(self.angle_rad, self.frequency_hz, self.voltage_pu, self.minimum_voltage) <= 0:
            raise ValueError("synchronization tolerances must be positive")

    def accepts(self, local, grid, local_hz, grid_hz):
        return bool(min(abs(local), abs(grid)) >= self.minimum_voltage
                    and abs(wrap_angle(np.angle(local)-np.angle(grid))) <= self.angle_rad
                    and abs(local_hz-grid_hz) <= self.frequency_hz
                    and abs(abs(local)-abs(grid)) <= self.voltage_pu)

def phase_correction(local, grid, gain=1.0, maximum_hz=.5):
    if gain < 0 or maximum_hz <= 0:
        raise ValueError("invalid synchronization controller")
    error = wrap_angle(np.angle(grid)-np.angle(local))
    return float(np.clip(gain*error/(2*np.pi), -maximum_hz, maximum_hz))
