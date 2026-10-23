import pytest

from gridlab.dc.conversion import dc_demand, rms_ll_ceiling


@pytest.mark.parametrize("ac_power", [10000, -10000])
def test_power_direction_preserves_dissipation(ac_power):
    dc, loss = dc_demand(ac_power, 20)
    assert dc - ac_power == pytest.approx(loss)
    assert loss > 0


def test_line_line_rms_limit_of_svpwm():
    assert rms_ll_ceiling(700) == pytest.approx(494.9747468)
