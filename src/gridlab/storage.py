"""Portable compressed NumPy archives; loading never enables pickle."""

import json
from pathlib import Path

import numpy as np

from .simulation import Result

_ARRAYS = ("time", "state", "voltage", "power", "frequency_hz", "current", "network_residual", "enabled")


def save_result(result, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as stream:
        np.savez_compressed(
            stream,
            schema_version=np.array(2),
            solver_options_json=np.array(json.dumps(result.solver_options, allow_nan=False)),
            source_names=np.array(result.source_names),
            nominal_hz=np.array(result.nominal_hz),
            **{key: getattr(result, key) for key in _ARRAYS},
        )


def load_result(path):
    with np.load(path, allow_pickle=False) as archive:
        if archive["schema_version"].item() != 2:
            raise ValueError("unsupported result schema")
        arrays = {key: archive[key].copy() for key in _ARRAYS}
        names = tuple(str(x) for x in archive["source_names"])
        nominal = float(archive["nominal_hz"])
        options = json.loads(str(archive["solver_options_json"]))
    n, count = len(arrays["time"]), len(names)
    if arrays["time"].ndim != 1 or n < 2 or np.any(np.diff(arrays["time"]) <= 0):
        raise ValueError("invalid archive time axis")
    if any(a.shape[0] != n for a in arrays.values()):
        raise ValueError("inconsistent archive sample counts")
    if any(arrays[key].shape != (n, count) for key in ("power", "frequency_hz", "current", "enabled")):
        raise ValueError("inconsistent source dimensions")
    return Result(source_names=names, nominal_hz=nominal, solver_options=options, **arrays)
