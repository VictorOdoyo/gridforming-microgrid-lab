import pytest
from gridlab.vsm import VSM

def test_initial_rocof_and_droop_equilibrium():
    v = VSM(5, 2, 50)
    assert v.derivative(0, .7, .5) == pytest.approx(-1)
    assert v.derivative(-.4, .7, .5) == pytest.approx(0, abs=1e-14)
    assert VSM(10, 2).derivative(0, .7, .5) == pytest.approx(-.5)
