import pytest
from gridlab.dclink import DCLink

def test_capacitor_energy_balance():
    c = DCLink(.01)
    v = c.step(700, 1000, 500, .1)
    assert c.energy(v)-c.energy(700) == pytest.approx(50)

def test_depletion_is_reported():
    with pytest.raises(RuntimeError):
        DCLink(.01).step(10, 0, 1000, 1)
