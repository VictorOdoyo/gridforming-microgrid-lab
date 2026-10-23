import pytest

from gridlab.hybrid.audit import audit_hybrid
from gridlab.hybrid.plant import HybridPlant
from gridlab.hybrid.simulation import simulate_hybrid


def test_solar_supplies_ac_load_and_charges_battery_through_same_dc_link():
    p = HybridPlant()
    r = simulate_hybrid(p, duration=0.2, conductance=lambda t: 0.1, solar=lambda t: 30000)
    a = audit_hybrid(p, r)
    assert r.state[-1, 0] > r.state[0, 0]
    assert a["solar_input_j"] == pytest.approx(6000)
    assert a["chemical_draw_j"] < 0
    assert a["relative_residual"] < 1e-3
