import numpy as np
import pytest
from gridlab.limited_network import solve_limited

def test_limited_resistive_source_has_exact_current_and_voltage():
    p = solve_limited([[1]], [0], [.1], [1], [.5])
    assert abs(p.current[0]) == pytest.approx(.5)
    assert p.voltage[0].real == pytest.approx(.5)
    assert p.residual < 1e-9

def test_unlimited_case_matches_voltage_divider():
    p = solve_limited([[1]], [0], [.1j], [1], [10])
    np.testing.assert_allclose(p.voltage, [1/(1+.1j)])
