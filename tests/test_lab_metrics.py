from gridlab.dc.system import DCSystem
from gridlab.lab.case import LabCase, run_case
from gridlab.lab.metrics import summarize


def test_physical_summary_carries_si_units_and_independent_energy_audit():
    c = LabCase("dc", "dc", "short DC run", DCSystem(), 0.01)
    r = run_case(c)
    m = summarize(c, r)
    assert 600 < m["minimum_dc_v"] < 710
    assert m["energy"]["relative_residual"] < 1e-3
    assert m["kind"] == "dc"
