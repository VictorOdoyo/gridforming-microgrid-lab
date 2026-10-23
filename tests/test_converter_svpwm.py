import numpy as np
import pytest

from gridlab.converter.svpwm import duties, reconstruct


def test_duty_reconstruction_across_all_six_space_vector_sectors():
    for angle in np.linspace(0, 2 * np.pi, 49):
        desired = 390 * np.exp(1j * angle)
        d = duties(desired, 700)
        assert d.min() >= 0 and d.max() <= 1
        assert reconstruct(d, 700) == pytest.approx(desired)


def test_overmodulation_is_limited_radially():
    assert abs(reconstruct(duties(1000j, 700), 700)) == pytest.approx(700 / np.sqrt(3))
