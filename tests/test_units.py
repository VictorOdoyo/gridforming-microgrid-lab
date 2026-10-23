import math

import pytest

from gridlab.units import Base


def test_three_phase_rating_and_impedance():
    b = Base()
    assert math.sqrt(3) * b.voltage_ll_v * b.current_a == pytest.approx(b.power_va)
    assert b.impedance_ohm == 1.6
    assert b.power_pu(50_000) == 0.5


@pytest.mark.parametrize("value", [0, -1, float("nan"), float("inf")])
def test_invalid_base(value):
    with pytest.raises(ValueError):
        Base(power_va=value)
