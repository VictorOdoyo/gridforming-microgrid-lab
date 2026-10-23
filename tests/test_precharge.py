import math

import pytest

from gridlab.protection.precharge import Precharge


def test_precharge_closing_time_and_resistor_energy():
    p = Precharge()
    time = -p.resistance_ohm * p.capacitance_f * math.log(1 - p.close_fraction)
    assert p.ready(time + 1e-9, 700)
    assert p.resistor_energy_j(200, 700) == pytest.approx(0.5 * 0.05 * 700**2)
    with pytest.raises(RuntimeError):
        p.ready(21, 700)
