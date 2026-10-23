from gridlab.lab.case import run_case
from gridlab.lab.cases import hybrid_step
from gridlab.lab.metrics import summarize
from gridlab.lab.timing import retime


def test_current_metrics_accept_all_thirteen_coupled_states():
    c = retime(hybrid_step(), 0.002)
    r = run_case(c)
    m = summarize(c, r)
    assert r.state.shape[1] == 13
    assert m["maximum_battery_a"] >= 0
    assert m["precharge_samples"] == 0
