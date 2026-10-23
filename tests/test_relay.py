from gridlab.relay import DefiniteTimeRelay


def test_pickup_timer_resets_and_trip_latches():
    r = DefiniteTimeRelay(49, 0.2)
    assert not r.step(48, 0.1)
    assert not r.step(50, 0.1)
    assert not r.step(48, 0.1)
    assert r.step(48, 0.1)
    assert r.step(50, 0.1)
    r.reset()
    assert not r.tripped
