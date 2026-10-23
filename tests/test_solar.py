from gridlab.solar import PVArray

def test_darkness_and_temperature_derating():
    pv = PVArray(100)
    assert pv.available_kw(0) == 0
    assert pv.available_kw(1000, 40) < pv.available_kw(1000, 20)
    assert pv.dispatch_kw(1000, limit_kw=20) == 20
