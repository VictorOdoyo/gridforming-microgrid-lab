"""Named reproducible experiments; all powers are on the shared system base."""
from dataclasses import dataclass, replace
from .config import Inverter, Microgrid, GridConnection
from .events import Event
from .network import Line

@dataclass(frozen=True)
class Case:
    name: str
    description: str
    config: Microgrid
    events: tuple
    duration: float

def load_step(mode="droop"):
    c = Microgrid(1, (), (.8+.2j,),
                  (Inverter("battery-a", 0, p_ref=.4, mode=mode),
                   Inverter("battery-b", 0, p_ref=.4, mode=mode)))
    return Case("load-step", "50 percent impedance-load increase at 2 s", c,
                (Event(2, "load_scale", 1.5),), 8)

CASES = {"load-step": load_step}

def secondary_restoration(mode="droop"):
    base = load_step(mode)
    return Case("secondary-restoration", "Load step with integral frequency restoration",
                replace(base.config, secondary_gain=1.0), base.events, 12)

CASES["secondary-restoration"] = secondary_restoration

def generator_trip(mode="vsm"):
    base = load_step(mode)
    return Case("generator-trip", "Trip battery-b at 2 s and restore frequency",
                replace(base.config, secondary_gain=.7),
                (Event(2, "source_enabled", 0, 1),), 12)

CASES["generator-trip"] = generator_trip

def black_start(mode="droop"):
    base = load_step(mode)
    c = replace(base.config, loads=(.1+.025j,), startup_s=1.5, secondary_gain=.5)
    return Case("black-start", "Ramp voltage from zero then pick up staged loads", c,
                (Event(2, "load_scale", 4), Event(4, "load_scale", 8)), 12)

CASES["black-start"] = black_start

def island_recovery(mode="vsm"):
    base = load_step(mode)
    c = replace(base.config, grid=GridConnection(initially_connected=False),
                secondary_gain=1.0, sync_gain=2.0)
    return Case("island-recovery", "Islanded generator trip followed by checked utility reconnection",
                c, (Event(2, "source_enabled", 0, 1), Event(16, "grid_enabled", 1)), 20)

CASES["island-recovery"] = island_recovery
