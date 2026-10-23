import numpy as np

from gridlab.hybrid.plant import HybridPlant
from gridlab.hybrid.simulation import simulate_hybrid


def test_battery_supplies_load_and_both_voltage_loops_recover():
    p = HybridPlant()
    r = simulate_hybrid(p)
    dc_v = np.sqrt(2 * r.state[:, 3] / p.dc.bus.capacitance_f)
    ac_v = r.state[:, 7] + 1j * r.state[:, 8]
    assert r.state[-1, 0] < r.state[0, 0]
    assert abs(dc_v[-1] - 700) < 3
    assert abs(ac_v[-1] - 325) < 1
    assert dc_v.min() > 600
    assert np.max(abs(r.command) - dc_v / 3**0.5) < 1
