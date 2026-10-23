import numpy as np
import pytest

from gridlab.current_limit import limit_current


@pytest.mark.parametrize("priority", ["radial", "active", "reactive"])
def test_limit_circle(priority):
    d, q = limit_current(2, 2, 1, priority)
    assert np.hypot(d, q) == pytest.approx(1)


def test_priority_retains_requested_axis():
    assert limit_current(0.8, 2, 1, "active") == pytest.approx((0.8, 0.6))
    assert limit_current(2, 0.8, 1, "reactive") == pytest.approx((0.6, 0.8))
