import numpy as np
from gridlab.secondary import secondary_rate, consensus_rate

def test_secondary_direction_and_antiwindup():
    assert secondary_rate([-.2, -.4], 0, 1, 2) > 0
    assert secondary_rate([-.2], 2, 1, 2) == 0
    assert secondary_rate([.2], 2, 1, 2) < 0

def test_consensus_preserves_mean_without_frequency_error():
    rate = consensus_rate([1, -1], [0, 0], [[1, -1], [-1, 1]], 1, .5)
    np.testing.assert_allclose(rate, [-1, 1])
