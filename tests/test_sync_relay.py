from gridlab.protection.sync_relay import SyncRelay


def test_intermittent_good_sync_does_not_satisfy_dwell():
    p = SyncRelay(dwell_s=0.2)
    assert not p.step(1, 1, 50, 50, 0.1)
    assert not p.step(1j, 1, 50, 50, 0.1)
    assert not p.step(1, 1, 50, 50, 0.1)
    assert p.step(1, 1, 50, 50, 0.1)
