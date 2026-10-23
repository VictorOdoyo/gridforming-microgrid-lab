"""Typed laboratory trace archives with object arrays forbidden."""

import json
from dataclasses import fields
from pathlib import Path

import numpy as np

from gridlab.converter.simulation import ConverterTrace
from gridlab.dc.simulation import DCTrace
from gridlab.hybrid.simulation import HybridTrace

_TYPES = {"dc": DCTrace, "converter": ConverterTrace, "hybrid": HybridTrace}


def validate_trace(kind, trace):
    if kind not in _TYPES or not isinstance(trace, _TYPES[kind]):
        raise ValueError("trace does not match selected laboratory kind")
    t = np.asarray(trace.time)
    if t.ndim != 1 or len(t) < 2 or np.any(np.diff(t) <= 0):
        raise ValueError("trace needs increasing time and at least two samples")
    for f in fields(trace):
        value = getattr(trace, f.name)
        if isinstance(value, str):
            continue
        a = np.asarray(value)
        if a.dtype.hasobject or a.shape[0] != len(t) or not np.isfinite(a).all():
            raise ValueError("finite numeric arrays with matching sample counts required")
    widths = {"dc": (5,), "converter": (4,), "hybrid": (9, 13)}
    if trace.state.ndim != 2 or trace.state.shape[1] not in widths[kind]:
        raise ValueError("state dimension does not match model")


def save_trace(kind, trace, path, metadata=None):
    validate_trace(kind, trace)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    arrays = {f.name: np.asarray(getattr(trace, f.name)) for f in fields(trace)}
    with path.open("wb") as stream:
        np.savez_compressed(
            stream,
            schema_version=np.array(1),
            kind=np.array(kind),
            metadata_json=np.array(json.dumps(metadata or {}, allow_nan=False)),
            **arrays,
        )


def load_trace(path):
    with np.load(path, allow_pickle=False) as archive:
        if archive["schema_version"].item() != 1:
            raise ValueError("unsupported laboratory trace schema")
        kind = str(archive["kind"])
        if kind not in _TYPES:
            raise ValueError("unknown archived laboratory kind")
        cls = _TYPES[kind]
        values = {f.name: archive[f.name].copy() for f in fields(cls)}
        if "termination" in values:
            values["termination"] = str(values["termination"])
        trace = cls(**values)
        metadata = json.loads(str(archive["metadata_json"]))
    validate_trace(kind, trace)
    return kind, trace, metadata
