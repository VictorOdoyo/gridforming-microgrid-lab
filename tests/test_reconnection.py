import numpy as np
import pytest
from gridlab.config import Inverter, Microgrid, GridConnection
from gridlab.events import Event, run_events
from gridlab.dynamics import Dynamics

def test_synchronized_no_load_island_can_reconnect():
    c = Microgrid(1, (), (0j,), (Inverter("a", 0, p_ref=0),),
                  grid=GridConnection(initially_connected=False))
    r = run_events(c, [Event(.1, "grid_enabled", 1)], .2)
    np.testing.assert_allclose(abs(r.voltage), 1)

def test_out_of_phase_reconnection_is_rejected():
    c = Microgrid(1, (), (0j,), (Inverter("a", 0, p_ref=0),),
                  grid=GridConnection(initially_connected=False))
    x = Dynamics(c).initial()
    x[0] = 1
    with pytest.raises(RuntimeError, match="synchronization"):
        run_events(c, [Event(.1, "grid_enabled", 1)], .2, initial=x)
