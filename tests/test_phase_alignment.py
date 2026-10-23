import numpy as np
from gridlab.config import Inverter, Microgrid, GridConnection
from gridlab.dynamics import Dynamics
from gridlab.events import Event, run_events

def test_phase_feedback_recovers_before_reclosing():
    c = Microgrid(1, (), (0j,), (Inverter("a", 0, p_ref=0),),
                  grid=GridConnection(initially_connected=False), sync_gain=2)
    x = Dynamics(c).initial()
    x[0] = 1
    r = run_events(c, [Event(3, "grid_enabled", 1)], 3.5, initial=x)
    k = np.flatnonzero(r.time == 3)[0]
    assert abs(np.angle(r.voltage[k, 0])) < .01
