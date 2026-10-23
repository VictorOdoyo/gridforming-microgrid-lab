from gridlab.lab.case import run_case
from gridlab.lab.cases import hybrid_cloud
from gridlab.lab.metrics import summarize


def test_solar_transition_reverses_battery_current_without_losing_ac_service():
    c = hybrid_cloud()
    r = run_case(c)
    assert r.state[:, 2].min() < 0 and r.state[-1, 2] > 0
    assert r.gate.all()
    m = summarize(c, r)
    assert m["energy"]["solar_input_j"] > 4000
    assert m["energy"]["relative_residual"] < 1e-3
