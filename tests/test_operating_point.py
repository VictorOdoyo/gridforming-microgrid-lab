import numpy as np
from gridlab.config import Inverter, Microgrid
from gridlab.operating_point import operating_point
from gridlab.dynamics import Dynamics

def test_island_equilibrium_has_common_frequency_and_power_balance():
    c = Microgrid(1, (), (.5+.1j,), (Inverter("a", 0, p_ref=.3),))
    p = operating_point(c)
    d = Dynamics(c)
    assert p.residual < 1e-7
    np.testing.assert_allclose(d.frequencies(p.state), p.common_deviation_hz, atol=1e-7)
    assert p.common_deviation_hz < 0

def test_secondary_equilibrium_restores_nominal_frequency():
    c = Microgrid(1, (), (.5+.1j,), (Inverter("a", 0, p_ref=.3, mode="vsm"),),
                  secondary_gain=1)
    p = operating_point(c)
    assert abs(p.common_deviation_hz) < 1e-8
