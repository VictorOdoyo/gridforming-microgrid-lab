import numpy as np
import pytest

from gridlab.phasors import complex_power, polar, power_factor, wrap_angle


def test_inductive_current_consumes_positive_reactive_power():
    s = complex_power(1, polar(1, -np.pi / 6))
    assert s.imag == pytest.approx(0.5)
    assert power_factor(s) == pytest.approx(np.sqrt(3) / 2)
    assert power_factor(0) == 0


def test_angle_wrap():
    assert wrap_angle(3 * np.pi) == pytest.approx(-np.pi)
