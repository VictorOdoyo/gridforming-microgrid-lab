from gridlab.lab.case import run_case
from gridlab.lab.cases import hybrid_low_soc
from gridlab.lab.metrics import summarize


def test_depleted_soc_reserve_cannot_behave_as_an_unlimited_ac_supply():
    c = hybrid_low_soc()
    r = run_case(c)
    assert r.state[-1, 0] < 0.11 and r.state[-1, 0] > 0.099
    assert not r.gate[-1]
    assert summarize(c, r)["energy"]["relative_residual"] < 1e-3
