"""Versioned laboratory JSON with explicit reconstruction of supported physical types."""

import json
from dataclasses import asdict
from pathlib import Path

from gridlab.converter.lc import LCPlant
from gridlab.dc.bidirectional import Bidirectional
from gridlab.dc.bus import Bus
from gridlab.dc.electrochem import Polarization
from gridlab.dc.events import DCEvent
from gridlab.dc.pack import Pack
from gridlab.dc.system import DCSystem
from gridlab.hybrid.events import HybridEvent
from gridlab.hybrid.grid_forming import GridForming
from gridlab.hybrid.plant import HybridPlant

from .case import LabCase
from .signals import Signal


def dc_plant(data):
    d = dict(data)
    p = dict(d.pop("pack", {}))
    for key in ("soc_points", "ocv_volts"):
        if key in p:
            p[key] = tuple(p[key])
    return DCSystem(
        pack=Pack(**p),
        bus=Bus(**d.pop("bus", {})),
        converter=Bidirectional(**d.pop("converter", {})),
        polarization=Polarization(**d.pop("polarization", {})),
        **d,
    )


def case_dict(case):
    return {"schema_version": 1, **asdict(case)}


def parse_case(data):
    d = dict(data)
    if d.pop("schema_version", None) != 1:
        raise ValueError("unsupported laboratory case schema")
    kind = d["kind"]
    raw = d.pop("plant")
    if kind == "dc":
        plant = dc_plant(raw)
    elif kind == "converter":
        plant = LCPlant(**raw)
    elif kind == "hybrid":
        raw = dict(raw)
        dc = dc_plant(raw.pop("dc", {}))
        ac = LCPlant(**raw.pop("ac", {}))
        outer = raw.pop("outer", None)
        plant = HybridPlant(dc=dc, ac=ac, outer=None if outer is None else GridForming(**outer), **raw)
    else:
        raise ValueError("unsupported laboratory kind")
    signals = {
        k: Signal(tuple(v["times"]), tuple(v["values"]), v.get("interpolation", "step"))
        for k, v in d.pop("signals", {}).items()
    }
    event_cls = DCEvent if kind == "dc" else HybridEvent
    events = tuple(event_cls(**e) for e in d.pop("events", ()))
    return LabCase(plant=plant, signals=signals, events=events, **d)


def save_case(case, path):
    Path(path).write_text(json.dumps(case_dict(case), indent=2, allow_nan=False) + "\n", encoding="utf-8")


def load_case(path):
    return parse_case(json.loads(Path(path).read_text(encoding="utf-8")))
