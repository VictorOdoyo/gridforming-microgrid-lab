from gridlab.lab.case import run_case
from gridlab.lab.cases import dc_hot_pack


def test_hot_pack_limits_commanded_current_before_hard_thermal_trip():
    r = run_case(dc_hot_pack())
    assert max(r.reference_a) <= 200 / 3 + 1e-8
    assert r.state[-1, 4] >= 55
    assert r.state[-1, 3] < r.state[0, 3]
