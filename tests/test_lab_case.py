import pytest

from gridlab.dc.system import DCSystem
from gridlab.lab.case import LabCase, run_case
from gridlab.lab.signals import Signal


def test_portable_dc_case_executes_its_held_demand_signal():
    c = LabCase(
        "small",
        "dc",
        "test case",
        DCSystem(),
        0.003,
        signals={"demand_w": Signal((0, 0.001025), (10000, 20000))},
    )
    r = run_case(c)
    assert r.demand_w[r.time == 0.001025][0] == 20000
    with pytest.raises(ValueError):
        LabCase("bad", "converter", "wrong model", DCSystem(), 1)
