from gridlab.hybrid.control import HybridControl
from gridlab.hybrid.plant import HybridPlant


def test_measured_dc_voltage_limits_ac_command():
    p = HybridPlant()
    c = HybridControl.tuned(p)
    x = p.initial()
    x[3] = p.dc.bus.energy(500)
    duty, command, closed = c.step(p, x, 325, 0.1, 0.00005)
    assert 0 <= duty <= 1 and closed
    assert abs(command) <= 500 / 3**0.5 + 1e-9
