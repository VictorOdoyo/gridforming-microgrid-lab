from types import SimpleNamespace

import numpy as np
import pytest

from gridlab.convergence import observed_order, trajectory_error


def test_interpolation_uses_time_and_order_matches_quadratic_error():
    reference = SimpleNamespace(time=np.array([0, 1, 2]), frequency_hz=np.array([[0], [1], [2]]))
    candidate = SimpleNamespace(time=np.array([0, 0.5, 1]), frequency_hz=np.array([[0], [0.5], [1]]))
    assert trajectory_error(reference, candidate)["max_abs"] == 0
    assert observed_order(0.04, 0.01) == pytest.approx(2)
