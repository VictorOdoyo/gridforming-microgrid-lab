import numpy as np
import pytest

from gridlab.converter.lc import LCPlant
from gridlab.converter.tuning import tune_lc


def test_current_pole_cancellation_and_outer_second_order_polynomial():
    p = LCPlant()
    k = tune_lc(p)
    assert k.current_ki / k.current_kp == pytest.approx(p.resistance_ohm / p.inductance_h)
    poles = np.roots([p.capacitance_f, k.voltage_kp, k.voltage_ki])
    assert np.all(poles.real < 0)
    with pytest.raises(ValueError):
        tune_lc(p, 100, 50)
