import pytest

from gridlab.dc.terminal import terminal_power


@pytest.mark.parametrize("power", [0, 10000, -10000, 1e-8])
def test_terminal_and_chemical_power_conservation(power):
    t = terminal_power(600, 0.1, power)
    assert t.power_w == pytest.approx(power)
    assert 600 * t.current_a == pytest.approx(t.power_w + t.copper_loss_w)


def test_maximum_power_and_current_are_enforced():
    t = terminal_power(600, 0.1, 1e9, 100)
    assert t.current_a == pytest.approx(100)
    assert t.limited
