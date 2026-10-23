import numpy as np
from gridlab.cases import generator_trip
from gridlab.events import run_events

def test_status_changes_on_exact_trip_time():
    c = generator_trip()
    r = run_events(c.config, c.events, 3, sample_s=.1, max_step=.05)
    assert r.enabled[r.time < 2].all()
    assert not r.enabled[r.time >= 2, 1].any()
    assert r.enabled[:, 0].all()
