import numpy as np
import pytest
from gridlab.norton import solve_network

def test_voltage_divider_and_kcl():
    point = solve_network([[1]], [0], [.1+.2j], [1])
    np.testing.assert_allclose(point.voltage, [1/(1.1+.2j)])
    np.testing.assert_allclose(point.current, point.voltage)
    assert point.residual < 1e-12

def test_parallel_identical_sources_share_equally():
    point = solve_network([[1]], [0, 0], [.1j, .1j], [1, 1])
    assert point.power[0] == pytest.approx(point.power[1])
