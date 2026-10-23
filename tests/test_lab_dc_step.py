from gridlab.lab.case import run_case
from gridlab.lab.cases import dc_step
from gridlab.lab.metrics import summarize


def test_named_dc_step_meets_recovery_and_energy_criteria():
    c = dc_step()
    m = summarize(c, run_case(c))
    assert m["termination"] == "completed"
    assert abs(m["final_dc_v"] - 700) < 5
    assert m["energy"]["relative_residual"] < 1e-4
