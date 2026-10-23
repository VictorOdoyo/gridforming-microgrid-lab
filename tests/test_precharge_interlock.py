import numpy as np
import pytest

from gridlab.dc.control import DCControl
from gridlab.dc.system import DCSystem


@pytest.mark.parametrize("soc,temperature", [(0.09, 25), (0.5, 80)])
def test_unhealthy_pack_cannot_energize_the_precharge_path(soc, temperature):
    p = DCSystem()
    x = p.initial(soc=soc, voltage=500)
    x[4] = temperature
    c = DCControl()
    duty, closed = c.step(p, x, 0, 0.0001, reset=True)
    assert not closed and not c.precharging and duty == 0


def test_main_contactor_rearm_requires_link_voltage_without_mutating_plant_state():
    p = DCSystem()
    c = DCControl()
    x = p.initial(voltage=500)
    c.step(p, x, 0, 0.0001, reset=True)
    assert c.precharging and not c.bms.closed
    x[3] = p.bus.energy(610)
    before = x.copy()
    _, closed = c.step(p, x, 0, 0.0001)
    assert closed and not c.precharging
    np.testing.assert_array_equal(x, before)
