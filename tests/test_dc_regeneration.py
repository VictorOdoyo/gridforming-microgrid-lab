import numpy as np

from gridlab.dc.audit import audit_dc
from gridlab.dc.simulation import simulate_dc
from gridlab.dc.system import DCSystem


def test_regenerative_load_charges_battery_without_creating_energy():
    p = DCSystem()
    r = simulate_dc(p, lambda t: -30000, 0.3)
    a = audit_dc(p, r)
    assert r.termination == "completed"
    assert r.state[-1, 0] > r.state[0, 0]
    assert r.state[-1, 2] < 0
    assert a["chemical_draw_j"] < 0 and a["delivered_j"] < 0
    assert a["heat_j"] > 0
    assert a["relative_residual"] < 1e-4
    assert np.sqrt(2 * r.state[-1, 3] / p.bus.capacitance_f) < 705
