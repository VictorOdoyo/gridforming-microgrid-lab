import pytest

from gridlab.battery import Battery


def test_discharge_conserves_energy_and_respects_reserve():
    b = Battery(10, 20, 20)
    soc, p = b.step(0.5, 20, 3600)
    assert soc == pytest.approx(0.1)
    assert p == pytest.approx(4 * 0.95)


def test_charge_losses_and_upper_bound():
    b = Battery(10, 20, 20)
    soc, p = b.step(0.8, -20, 3600)
    assert soc == pytest.approx(0.9)
    assert p == pytest.approx(-1 / 0.95)
