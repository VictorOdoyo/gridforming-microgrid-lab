import numpy as np

from gridlab.dc.simulation import simulate_dc
from gridlab.dc.system import DCSystem


def test_cascaded_dc_control_recovers_voltage_after_power_step():
    p = DCSystem()
    r = simulate_dc(p, lambda t: 30000 if t < 0.1 else 60000, 0.5)
    voltage = np.sqrt(2 * r.state[:, 3] / p.bus.capacitance_f)
    assert r.termination == "completed"
    assert abs(voltage[-1] - 700) < 5
    assert voltage.min() > 600
    assert np.max(r.state[:, 2]) < 200
    assert r.state[-1, 0] < 0.5
