from gridlab.lab.case import run_case
from gridlab.lab.cases import hybrid_outage
from gridlab.lab.metrics import summarize


def test_named_outage_reports_isolation_and_energy_conservation():
    c = hybrid_outage()
    r = run_case(c)
    m = summarize(c, r)
    assert not r.gate[-1]
    assert m["gate_blocked_samples"] > 0
    assert m["final_ac_ll_rms_v"] < 1
    assert m["energy"]["relative_residual"] < 1e-3
