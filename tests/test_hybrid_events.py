import numpy as np

from gridlab.hybrid.events import HybridEvent
from gridlab.hybrid.simulation import simulate_hybrid


def test_hybrid_noninteger_load_event_is_applied_at_exact_time():
    r = simulate_hybrid(duration=0.03, events=(HybridEvent(0.020025, "conductance", 0.15),))
    k = np.flatnonzero(r.time == 0.020025)[0]
    assert r.conductance[k - 1] == 0.1 and r.conductance[k] == 0.15
    assert np.diff(r.time).min() > 0
