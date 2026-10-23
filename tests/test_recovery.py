from gridlab.recovery import settling_time


def test_recovery_requires_remaining_in_band():
    assert settling_time([0, 1, 2, 3, 4], [2, 1, 2, 1, 1], 1, 0.1) == 3
    assert settling_time([0, 1, 2], [2, 1, 2], 1, 0.1) is None
    assert settling_time([0, 1, 2], [2, 1, 1], 1, 0.1, hold_s=2) is None
