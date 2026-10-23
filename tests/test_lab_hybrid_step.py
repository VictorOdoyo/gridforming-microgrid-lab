from gridlab.lab.case import run_case
from gridlab.lab.cases import hybrid_step
from gridlab.lab.metrics import summarize


def test_named_hybrid_step_recovers_both_voltage_loops_with_energy_closure():
    c = hybrid_step()
    m = summarize(c, run_case(c))
    assert abs(m["final_dc_v"] - 700) < 4
    assert m["final_tracking_error_peak_v"] < 2
    assert m["energy"]["relative_residual"] < 1e-3
    assert m["final_soc"] < m["initial_soc"]
