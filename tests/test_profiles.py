import numpy as np
import pytest
from gridlab.profiles import Profile, ramp

def test_interpolation_and_endpoint_hold():
    p = Profile((0, 2, 4), (0, 1, .5))
    np.testing.assert_allclose(p([-1, 1, 3, 8]), [0, .5, .75, .5])
    np.testing.assert_allclose(ramp([-1, 1, 3], 0, 2), [0, .5, 1])

def test_duplicate_times_rejected():
    with pytest.raises(ValueError):
        Profile((0, 0), (1, 2))
