import numpy as np
import pytest
from gridlab.loads import ZIPLoad
from gridlab.zip_network import solve_zip

def test_constant_power_voltage_matches_quadratic_root():
    p = solve_zip([[0]], [0], [.1], [1], [ZIPLoad(.5, 0, 0, 1)])
    assert p.voltage[0].real == pytest.approx((1+np.sqrt(.8))/2)
    assert p.power[0].real == pytest.approx(.5)
