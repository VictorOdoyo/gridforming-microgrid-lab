import pytest
from gridlab.thermal import ThermalRC, converter_loss

def test_thermal_equilibrium_and_cooling():
    t = ThermalRC(.2, 10)
    assert t.step(25, 25, 100, 100) == pytest.approx(45)
    assert 25 < t.step(45, 25, 0, 1) < 45
    assert converter_loss(20, 600, 10000) > converter_loss(10, 600, 10000)
