from gridlab.protection.i2t import I2T


def test_two_times_pickup_trips_at_one_third_threshold_time():
    p = I2T(100, 3)
    for _ in range(99):
        assert not p.step(200, 0.01)
    assert p.step(200, 0.01)
    p.reset()
    p.step(150, 0.1)
    before = p.stress
    p.step(0, 0.1)
    assert p.stress < before
