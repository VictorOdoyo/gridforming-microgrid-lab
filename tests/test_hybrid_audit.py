from gridlab.hybrid.audit import audit_hybrid
from gridlab.hybrid.plant import HybridPlant
from gridlab.hybrid.simulation import simulate_hybrid


def test_full_battery_to_load_energy_balance_closes():
    p = HybridPlant()
    r = simulate_hybrid(p, duration=0.15)
    audit = audit_hybrid(p, r)
    assert audit["served_load_j"] > 1000
    assert audit["loss_j"] > 0
    assert audit["relative_residual"] < 5e-4
