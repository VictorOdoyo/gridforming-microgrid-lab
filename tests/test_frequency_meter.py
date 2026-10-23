import numpy as np
import pytest

from gridlab.protection.frequency import FrequencyMeter


def test_phasor_frequency_and_low_voltage_reset():
    f = FrequencyMeter()
    assert f.step(1, 0.01) is None
    assert f.step(np.exp(-2j * np.pi * 0.2 * 0.01), 0.01) == pytest.approx(49.8)
    assert f.step(0, 0.01) is None
    assert f.step(1, 0.01) is None
