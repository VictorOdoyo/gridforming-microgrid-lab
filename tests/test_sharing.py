import numpy as np
import pytest
from gridlab.sharing import equilibrium, rating_scaled_droop

def test_two_to_one_ratings_share_increment_two_to_one():
    gains = rating_scaled_droop([2, 1])
    df, power = equilibrium(.9, [0, 0], gains)
    assert df == pytest.approx(-.3)
    np.testing.assert_allclose(power, [.6, .3])
    assert sum(power) == pytest.approx(.9)
