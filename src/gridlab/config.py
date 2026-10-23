"""Validated immutable phasor-simulation configuration."""
from dataclasses import dataclass, field
import numpy as np
from .network import Line
from .units import Base

@dataclass(frozen=True)
class Inverter:
    name: str
    bus: int
    impedance: complex = .02+.15j
    p_ref: float = .3
    q_ref: float = 0.0
    v_ref: float = 1.0
    droop_hz: float = 1.0
    q_droop: float = .05
    inertia_s: float = 2.0
    power_tau: float = .02
    voltage_tau: float = .1
    mode: str = "droop"
    rating_pu: float = 1.0
    current_limit_pu: float = float("inf")

    def __post_init__(self):
        if not self.name or self.bus < 0 or self.mode not in ("droop", "vsm"):
            raise ValueError("invalid inverter identity or mode")
        numeric = [self.impedance.real, self.impedance.imag, self.p_ref, self.q_ref,
                   self.v_ref, self.droop_hz, self.q_droop, self.inertia_s,
                   self.power_tau, self.voltage_tau, self.rating_pu]
        if not np.all(np.isfinite(numeric)):
            raise ValueError("inverter values must be finite")
        if self.current_limit_pu <= 0 or np.isnan(self.current_limit_pu):
            raise ValueError("current limit must be positive")
        if abs(self.impedance) == 0 or self.impedance.real < 0:
            raise ValueError("invalid output impedance")
        if min(self.v_ref, self.droop_hz, self.inertia_s, self.power_tau,
               self.voltage_tau, self.rating_pu) <= 0 or self.q_droop < 0:
            raise ValueError("invalid controller gains or ratings")

@dataclass(frozen=True)
class GridConnection:
    bus: int = 0
    impedance: complex = .02+.1j
    voltage: complex = 1+0j
    initially_connected: bool = True

    def __post_init__(self):
        if self.bus < 0 or abs(self.impedance) == 0 or self.impedance.real < 0:
            raise ValueError("invalid grid connection")
        if not np.isfinite(self.voltage) or not np.isfinite(self.impedance) or abs(self.voltage) == 0:
            raise ValueError("grid voltage and impedance must be finite and nonzero")

@dataclass(frozen=True)
class Microgrid:
    nbus: int
    lines: tuple[Line, ...]
    loads: tuple[complex, ...]
    inverters: tuple[Inverter, ...]
    base: Base = field(default_factory=Base)
    grid: GridConnection | None = None
    startup_s: float = 0.0
    sync_gain: float = 0.0
    secondary_gain: float = 0.0
    secondary_limit_hz: float = 2.0

    def __post_init__(self):
        if self.nbus < 1 or len(self.loads) != self.nbus or not self.inverters:
            raise ValueError("invalid bus, load, or source count")
        if any(x.bus >= self.nbus for x in self.inverters):
            raise ValueError("inverter bus out of range")
        if len({x.name for x in self.inverters}) != len(self.inverters):
            raise ValueError("inverter names must be unique")
        if any(max(x.start, x.end) >= self.nbus for x in self.lines):
            raise ValueError("line bus out of range")
        if not np.all(np.isfinite(self.loads)) or any(x.real < 0 for x in self.loads):
            raise ValueError("loads must be finite with nonnegative conductance")
        if self.grid is not None and self.grid.bus >= self.nbus:
            raise ValueError("grid bus out of range")
        if self.startup_s < 0 or not np.isfinite(self.startup_s):
            raise ValueError("invalid startup duration")
        if self.sync_gain < 0 or not np.isfinite(self.sync_gain):
            raise ValueError("invalid synchronization gain")
        if self.secondary_gain < 0 or self.secondary_limit_hz <= 0:
            raise ValueError("invalid secondary control")
