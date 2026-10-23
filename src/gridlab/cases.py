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
