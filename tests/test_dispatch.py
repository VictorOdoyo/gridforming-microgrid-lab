import pytest
from gridlab.battery import Battery
from gridlab.dispatch import dispatch

@pytest.mark.parametrize("load,pv,soc", [(80, 10, .5), (10, 80, .9), (100, 0, .1)])
def test_dispatch_conservation(load, pv, soc):
    d = dispatch(load, pv, Battery(100, 30, 30), soc, 40, 60)
    assert d.solar_kw+d.battery_kw+d.diesel_kw+d.unmet_kw == pytest.approx(load)
    assert d.solar_kw+d.curtailed_kw == pytest.approx(pv)
    assert .1 <= d.soc <= .9
