"""Versioned JSON case interchange; complex numbers are [real, imag] pairs."""
from dataclasses import asdict
import json
import tomllib
from pathlib import Path
from .cases import Case
from .config import Inverter, Microgrid, GridConnection
from .events import Event
from .network import Line
from .units import Base

def encode(value):
    if isinstance(value, complex):
        return [value.real, value.imag]
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    if isinstance(value, float) and value == float("inf"):
        return None
    return value

def case_dict(case):
    return {"schema_version": 1, **encode(asdict(case))}

def parse_case(data):
    data = dict(data)
    if data.pop("schema_version", None) != 1:
        raise ValueError("unsupported case schema")
    raw = dict(data.pop("config"))
    raw["loads"] = tuple(complex(*z) for z in raw["loads"])
    raw["lines"] = tuple(Line(**line) for line in raw.get("lines", ()))
    sources = []
    for source in raw["inverters"]:
        source = dict(source)
        if "impedance" in source:
            source["impedance"] = complex(*source["impedance"])
        if source.get("current_limit_pu", 1) is None:
            source["current_limit_pu"] = float("inf")
        sources.append(Inverter(**source))
    raw["inverters"] = tuple(sources)
    raw["base"] = Base(**raw.get("base", {}))
    if raw.get("grid") is not None:
        grid = dict(raw["grid"])
        for key in ("impedance", "voltage"):
            if key in grid:
                grid[key] = complex(*grid[key])
        raw["grid"] = GridConnection(**grid)
    events = tuple(Event(**e) for e in data.pop("events", ()))
    return Case(config=Microgrid(**raw), events=events, **data)

def save_case(case, path):
    Path(path).write_text(json.dumps(case_dict(case), indent=2, allow_nan=False)+"\n", encoding="utf-8")

def load_case(path):
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    return parse_case(tomllib.loads(text) if path.suffix.lower() == ".toml" else json.loads(text))
