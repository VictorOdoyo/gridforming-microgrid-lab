import numpy as np

from gridlab.energy import energy_kwh, source_losses


def test_one_hour_half_rating_is_fifty_kwh():
    np.testing.assert_allclose(energy_kwh([0, 3600], [[0.5, 0.2], [0.5, 0.2]], 100000), [50, 20])
    np.testing.assert_allclose(source_losses([0, 3600], [[1], [1]], [0.01 + 0.1j], 100000), [1])
