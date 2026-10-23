"""Case metadata separates signals and events from physical plant parameters."""

import math
from dataclasses import dataclass, field

from gridlab.converter.lc import LCPlant
from gridlab.converter.simulation import simulate_converter
from gridlab.dc.simulation import simulate_dc
from gridlab.dc.system import DCSystem
from gridlab.hybrid.plant import HybridPlant
from gridlab.hybrid.simulation import simulate_hybrid


@dataclass(frozen=True)
class LabCase:
    name: str
    kind: str
    description: str
    plant: object
    duration: float
    period_s: float = 0.00005
    signals: dict = field(default_factory=dict)
    events: tuple = ()
    initial_state: tuple | None = None

    def __post_init__(self):
        classes = {"dc": DCSystem, "converter": LCPlant, "hybrid": HybridPlant}
        if self.kind not in classes or not isinstance(self.plant, classes[self.kind]):
            raise ValueError("case kind must match its physical plant")
        if not self.name or not all(math.isfinite(v) and v > 0 for v in (self.duration, self.period_s)):
            raise ValueError("named case and positive finite timing required")
        if self.duration / self.period_s > 2_000_000:
            raise ValueError("case exceeds two million control intervals")
        from gridlab.dc.events import DCEvent
        from gridlab.hybrid.events import HybridEvent

        from .signals import Signal

        if any(not isinstance(s, Signal) for s in self.signals.values()):
            raise ValueError("signals must use the serializable Signal type")
        event_type = DCEvent if self.kind == "dc" else HybridEvent
        if any(not isinstance(e, event_type) for e in self.events):
            raise ValueError("supervisor event type does not match physical model")
        if self.initial_state is not None:
            expected = (
                5 if self.kind == "dc" else 4 if self.kind == "converter" else len(self.plant.initial())
            )
            if len(self.initial_state) != expected or not all(math.isfinite(v) for v in self.initial_state):
                raise ValueError("initial state does not match physical model")
        allowed = {
            "dc": {"demand_w"},
            "converter": {"reference_v", "conductance", "dc_voltage_v"},
            "hybrid": {"reference_v", "conductance", "solar_w"},
        }
        if set(self.signals) - allowed[self.kind]:
            raise ValueError("unknown signal for selected laboratory kind")
        if self.kind == "converter" and self.events:
            raise ValueError("converter cases use signals instead of supervisor events")
        if any(e.time > self.duration for e in self.events):
            raise ValueError("event outside case duration")
        for name, signal in self.signals.items():
            if name != "demand_w" and min(signal.values) < 0:
                raise ValueError("negative physical signal not supported")
            if name == "dc_voltage_v" and min(signal.values) <= 0:
                raise ValueError("converter DC supply must remain positive")
        if any(s.times[-1] > self.duration for s in self.signals.values()):
            raise ValueError("signal extends beyond case duration")


def run_case(case):
    bounds = sorted({t for s in case.signals.values() for t in s.times})
    common = {"duration": case.duration, "period_s": case.period_s, "boundaries": bounds}
    signals = case.signals
    if case.initial_state is not None:
        common["initial"] = case.initial_state
    if case.kind == "dc":
        return simulate_dc(case.plant, demand=signals.get("demand_w"), events=case.events, **common)
    if case.kind == "converter":
        return simulate_converter(
            case.plant,
            reference=signals.get("reference_v"),
            conductance=signals.get("conductance"),
            dc_voltage=signals.get("dc_voltage_v"),
            **common,
        )
    return simulate_hybrid(
        case.plant,
        reference=signals.get("reference_v"),
        conductance=signals.get("conductance"),
        solar=signals.get("solar_w"),
        events=case.events,
        **common,
    )
