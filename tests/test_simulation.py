import numpy as np

from gridlab.config import Inverter, Microgrid
from gridlab.simulation import simulate


def test_balanced_equilibrium_remains_constant():
    c = Microgrid(1, (), (0j,), (Inverter("a", 0, p_ref=0),))
    r = simulate(c, 0.23, 0.1)
    np.testing.assert_allclose(r.frequency_hz, 50)
    np.testing.assert_allclose(abs(r.voltage), 1)
    assert r.time[-1] == 0.23


def test_loaded_voltage_and_frequency_settle():
    c = Microgrid(1, (), (0.5 + 0.1j,), (Inverter("a", 0, p_ref=0.5),))
    r = simulate(c, 2)
    assert np.all(np.isfinite(r.state))
    assert 0.8 < abs(r.voltage[-1, 0]) < 1.1
