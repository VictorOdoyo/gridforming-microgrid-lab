import numpy as np
from gridlab.network import Line, admittance

def test_two_bus_stamp_and_kcl():
    y = admittance(2, [Line(0, 1, .1, .2)])
    np.testing.assert_allclose(y @ np.ones(2), 0, atol=1e-14)
    np.testing.assert_allclose(y, y.T)
    np.testing.assert_allclose(y @ [1, 0], [2-4j, -2+4j])

def test_pi_charging():
    y = admittance(2, [Line(0, 1, .1, .2, .02)])
    np.testing.assert_allclose(y @ np.ones(2), [.01j, .01j])
