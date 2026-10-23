from dataclasses import replace

import pytest

from gridlab.hybrid.events import HybridEvent
from gridlab.lab.case import run_case
from gridlab.lab.cases import dc_step
from gridlab.lab.config_io import load_case, save_case


def test_explicit_initial_state_roundtrips_and_drives_the_actual_plant(tmp_path):
    c = dc_step()
    initial = tuple(c.plant.initial(soc=0.2, voltage=680))
    c = replace(c, duration=0.002, signals={}, initial_state=initial)
    path = tmp_path / "case.json"
    save_case(c, path)
    loaded = load_case(path)
    assert loaded == c
    assert run_case(loaded).state[0, 0] == 0.2
    with pytest.raises(ValueError, match="event"):
        replace(c, events=(HybridEvent(0.001, "battery-trip"),))
