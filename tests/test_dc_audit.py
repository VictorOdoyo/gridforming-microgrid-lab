from gridlab.dc.audit import audit_dc
from gridlab.dc.simulation import simulate_dc
from gridlab.dc.system import DCSystem


def test_coupled_dc_energy_closes_independently_of_controller_equations():
    p = DCSystem()
    r = simulate_dc(p, duration=0.1)
    audit = audit_dc(p, r)
    assert audit["relative_residual"] < 1e-4
    assert abs(audit["thermal_residual_j"]) < 0.1
    assert audit["heat_j"] > 0
