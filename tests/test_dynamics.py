import numpy as np

from gridlab.config import Inverter, Microgrid
from gridlab.dynamics import Dynamics


def test_no_load_reference_is_exact_equilibrium():
    c = Microgrid(1, (), (0j,), (Inverter("a", 0, p_ref=0),))
    d = Dynamics(c)
    x = d.initial()
    np.testing.assert_allclose(d(0, x), 0, atol=1e-12)


def test_positive_load_produces_negative_frequency_deviation():
    c = Microgrid(1, (), (0.5 + 0j,), (Inverter("a", 0, p_ref=0),))
    d = Dynamics(c)
    assert d.frequencies(d.initial())[0] < 0
