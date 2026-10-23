import numpy as np

from gridlab.hybrid.audit import audit_hybrid
from gridlab.hybrid.events import HybridEvent
from gridlab.hybrid.plant import HybridPlant
from gridlab.hybrid.simulation import simulate_hybrid


def test_battery_trip_blocks_ac_before_dc_energy_collapses():
    p = HybridPlant()
    r = simulate_hybrid(p, duration=0.5, events=(HybridEvent(0.1, "battery-trip"),))
    assert not r.closed[r.time >= 0.1].any()
    assert not r.gate[-1]
    dc_v = np.sqrt(2 * r.state[:, 3] / p.dc.bus.capacitance_f)
    assert dc_v[-1] > 400
    assert abs(complex(*r.state[-1, 7:9])) < 1
    assert audit_hybrid(p, r)["relative_residual"] < 1e-3
