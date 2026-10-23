from gridlab.lab.case import run_case
from gridlab.lab.cases import hybrid_restart
from gridlab.lab.metrics import summarize


def test_named_restart_restores_physical_power_path_after_blocking():
    c = hybrid_restart()
    r = run_case(c)
    m = summarize(c, r)
    assert (~r.gate).any() and r.gate[-1] and r.closed[-1]
    assert m["final_ac_ll_rms_v"] > 390
    assert abs(m["final_dc_v"] - 700) < 5
    assert m["energy"]["relative_residual"] < 1e-3
