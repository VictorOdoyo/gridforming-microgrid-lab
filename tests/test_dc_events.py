import numpy as np

from gridlab.dc.events import DCEvent
from gridlab.dc.simulation import simulate_dc


def test_noninteger_event_time_is_saved_and_applied_exactly():
    r = simulate_dc(duration=0.02, events=(DCEvent(0.01005, "demand_w", 10000),))
    k = np.flatnonzero(r.time == 0.01005)[0]
    assert r.demand_w[k - 1] == 50000
    assert r.demand_w[k] == 10000
    assert np.all(np.diff(r.time) > 0)
