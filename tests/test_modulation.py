import numpy as np
import pytest

from gridlab.modulation import voltage_command


def test_svpwm_limit_preserves_angle():
    v = voltage_command(1000 * np.exp(0.7j), 700)
    assert abs(v) == pytest.approx(700 / np.sqrt(3))
    assert np.angle(v) == pytest.approx(0.7)
    assert voltage_command(0, 0) == 0
