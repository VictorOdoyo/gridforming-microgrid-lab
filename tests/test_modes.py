import numpy as np
import pytest
from gridlab.modes import modes, spectral_abscissa

def test_damped_pair_and_neutral_mode():
    a = np.array([[-1, -2, 0], [2, -1, 0], [0, 0, 0]])
    result = modes(a)
    assert result[0]["classification"] == "neutral"
    assert result[1]["damping_ratio"] == pytest.approx(1/np.sqrt(5))
    assert spectral_abscissa(a) == pytest.approx(-1)
    assert spectral_abscissa(a, exclude_neutral=False) == 0
