import numpy as np
import pytest

from gridlab.lab.signals import Signal


def test_right_continuous_hold_and_linear_signal_rounding():
    s = Signal((0, 0.137, 1), (1, 2, 0))
    np.testing.assert_allclose(s([0.136, 0.137, 0.9, 2]), [1, 2, 2, 0])
    assert Signal((0, 1), (0, 10), "linear")(0.5) == 5
    with pytest.raises(ValueError):
        Signal((0.1, 1), (0, 1))
