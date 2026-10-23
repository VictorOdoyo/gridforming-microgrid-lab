import numpy as np

from gridlab.config import Inverter, Microgrid
from gridlab.events import Event, run_events


def test_load_step_enters_current_limit_without_kcl_error():
    c = Microgrid(1, (), (0.3 + 0j,), (Inverter("a", 0, impedance=0.1 + 0j, current_limit_pu=0.5),))
    r = run_events(c, [Event(0.1, "load_scale", 5)], 0.3)
    assert np.max(abs(r.current)) <= 0.5 + 1e-9
    assert max(r.network_residual) < 1e-8
    assert abs(r.voltage[-1, 0]) < 0.4
