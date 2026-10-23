from gridlab.lab.case import run_case
from gridlab.lab.cases import hybrid_secondary
from gridlab.lab.metrics import summarize


def test_physical_vsm_secondary_control_removes_final_frequency_offset():
    c = hybrid_secondary()
    m = summarize(c, run_case(c))
    assert abs(m["final_internal_hz"] - 50) < 0.01
    assert m["energy"]["relative_residual"] < 1e-3
