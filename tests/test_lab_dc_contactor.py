from gridlab.lab.case import run_case
from gridlab.lab.cases import dc_contactor
from gridlab.lab.metrics import summarize


def test_named_contactor_experiment_preserves_energy_through_switching():
    c = dc_contactor()
    r = run_case(c)
    assert not r.closed[(r.time >= 0.05) & (r.time < 0.06)].any()
    assert r.closed[-1]
    assert summarize(c, r)["energy"]["relative_residual"] < 1e-4
