import json
from dataclasses import fields

import numpy as np
import pytest

from gridlab.dc.simulation import simulate_dc
from gridlab.dc.system import DCSystem
from gridlab.lab.case import LabCase, run_case
from gridlab.lab.metrics import summarize
from gridlab.lab.storage import load_trace


def test_precharge_current_is_distinct_from_offline_inductor_current():
    p = DCSystem()
    c = LabCase("precharge", "dc", "rearm", p, 0.005, 0.0001, initial_state=tuple(p.initial(voltage=500)))
    r = run_case(c)
    m = summarize(c, r)
    assert m["maximum_dc_inductor_a"] == 0
    assert m["maximum_battery_a"] > 40
    assert m["precharge_samples"] == len(r.time)


def test_version_one_archive_without_precharge_is_still_readable(tmp_path):
    r = simulate_dc(duration=0.002)
    values = {f.name: np.asarray(getattr(r, f.name)) for f in fields(r) if f.name != "precharge"}
    path = tmp_path / "old.npz"
    np.savez(path, schema_version=1, kind="dc", metadata_json=json.dumps({}), **values)
    kind, loaded, _ = load_trace(path)
    assert kind == "dc" and not loaded.precharge.any()


def test_dead_dc_capacitor_requires_analytical_initialization():
    with pytest.raises(ValueError, match="precharge"):
        simulate_dc(duration=0.001, initial=DCSystem().initial(voltage=0))
