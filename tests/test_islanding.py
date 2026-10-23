import numpy as np

from gridlab.config import GridConnection, Inverter, Microgrid
from gridlab.events import Event, run_events


def test_islanding_removes_utility_injection():
    c = Microgrid(1, (), (0.5 + 0j,), (Inverter("a", 0, p_ref=0.2),), grid=GridConnection())
    r = run_events(c, [Event(0.3, "grid_enabled", 0)], 0.6)
    for k in np.flatnonzero(r.time >= 0.3):
        np.testing.assert_allclose(r.current[k, 0], 0.5 * r.voltage[k, 0], atol=1e-10)
