import numpy as np
import pytest

from gridlab.spectrum import amplitude_spectrum, coherent_thd


def test_known_third_harmonic_and_dc_amplitude():
    t = np.arange(1000) / 10000
    x = 2 + np.sin(2 * np.pi * 50 * t) + 0.1 * np.sin(2 * np.pi * 150 * t)
    assert coherent_thd(x, 10000, 50) == pytest.approx(0.1)
    _, a = amplitude_spectrum(x, 10000, "rectangular")
    assert a[0] == pytest.approx(2)
