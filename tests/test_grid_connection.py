import numpy as np
from gridlab.config import Inverter, Microgrid, GridConnection
from gridlab.dynamics import Dynamics

def test_grid_supplies_load_when_inverter_is_disabled():
    c = Microgrid(1, (), (.5+.1j,), (Inverter("a", 0),), grid=GridConnection())
    d = Dynamics(c, enabled=[False])
    p = d.network(d.initial())
    np.testing.assert_allclose(p.voltage, [1/(1+c.grid.impedance*(.5-.1j))])
    assert p.power[0] == 0

def test_disconnected_grid_does_not_inject():
    c = Microgrid(1, (), (.5+0j,), (Inverter("a", 0),), grid=GridConnection())
    d = Dynamics(c, grid_connected=False)
    p = d.network(d.initial())
    np.testing.assert_allclose(p.current[0], .5*p.voltage[0])
