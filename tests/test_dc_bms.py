from gridlab.dc.bms import BMS


def test_contactors_remain_open_until_explicit_healthy_reset():
    b = BMS()
    assert not b.step(0.09, 25)
    assert not b.step(0.12, 25, reset=True)
    assert b.step(0.2, 25, reset=True)
    assert not b.step(0.5, 61)
    assert not b.step(0.5, 55, reset=True)
    assert b.step(0.5, 49, reset=True)
