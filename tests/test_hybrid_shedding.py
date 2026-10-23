from gridlab.hybrid.plant import HybridPlant
from gridlab.hybrid.simulation import simulate_hybrid
from gridlab.protection.shedding import StagedShedding


def test_sustained_overload_can_disconnect_noncritical_load_stages():
    p = HybridPlant()
    r = simulate_hybrid(
        p,
        duration=0.15,
        conductance=lambda t: 5 if t >= 0.05 else 0.1,
        shedding=StagedShedding(thresholds=(0.95,), fractions=(0.5,), delays_s=(0.005,)),
    )
    assert r.conductance[-1] == 2.5
    assert not r.gate[-1] or abs(complex(*r.state[-1, 7:9])) < 325
