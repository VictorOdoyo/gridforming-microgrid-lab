import numpy as np
import pytest

from gridlab.grid_strength import lossless_synchronizing_gain, short_circuit_ratio, transfer_power


def test_lossless_power_angle_and_synchronizing_torque():
    assert short_circuit_ratio(0.2j, 1) == 5
    assert transfer_power(1, 1, 0.2j, np.pi / 6).real == pytest.approx(2.5)
    assert lossless_synchronizing_gain(1, 1, 0.2, np.pi / 2) == pytest.approx(0, abs=1e-12)
