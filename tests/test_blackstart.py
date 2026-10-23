import numpy as np

from gridlab.config import Inverter, Microgrid
from gridlab.simulation import simulate


def test_black_start_builds_voltage_from_zero():
    c = Microgrid(1, (), (0.4 + 0.1j,), (Inverter("a", 0, p_ref=0.4),), startup_s=1)
    r = simulate(c, 3)
    assert abs(r.voltage[0, 0]) == 0
    assert abs(r.voltage[-1, 0]) > 0.9
    assert np.all(np.isfinite(r.state))
    assert abs(r.voltage).max() < 1.05
