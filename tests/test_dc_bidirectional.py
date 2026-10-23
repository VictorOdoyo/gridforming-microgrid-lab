import pytest

from gridlab.dc.bidirectional import Bidirectional


@pytest.mark.parametrize("current", [-100, 100])
def test_converter_energy_balance_in_both_directions(current):
    c = Bidirectional()
    di = c.derivative(current, 600, 700, 0.8)
    input_w = 600 * current
    output_w = 700 * c.bus_current(current, 0.8)
    assert input_w - output_w == pytest.approx(c.inductance_h * current * di + c.loss_w(current))
