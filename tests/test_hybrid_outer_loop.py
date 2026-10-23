from gridlab.hybrid.audit import audit_hybrid
from gridlab.hybrid.grid_forming import GridForming
from gridlab.hybrid.plant import HybridPlant
from gridlab.hybrid.simulation import simulate_hybrid


def test_grid_forming_angle_changes_physical_ac_reference_and_energy_still_closes():
    p = HybridPlant(outer=GridForming(mode="vsm"))
    r = simulate_hybrid(p, duration=0.25)
    assert r.state.shape[1] == 13
    assert abs(r.state[-1, 9]) > 0.001
    assert abs(p.outer.deviation(r.state[-1, 9:13])) < 0.1
    assert audit_hybrid(p, r)["relative_residual"] < 1e-3
