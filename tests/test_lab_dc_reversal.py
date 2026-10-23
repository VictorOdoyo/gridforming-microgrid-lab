from gridlab.lab.case import run_case
from gridlab.lab.cases import dc_reversal
from gridlab.lab.metrics import summarize


def test_reversal_reduces_net_chemical_draw_and_finishes_charging():
    c = dc_reversal()
    r = run_case(c)
    assert r.state[-1, 2] < 0
    m = summarize(c, r)
    assert m["energy"]["chemical_draw_j"] < 0
    assert m["energy"]["relative_residual"] < 1e-4
