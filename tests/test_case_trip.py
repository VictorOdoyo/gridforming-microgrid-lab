import numpy as np
from gridlab.cases import generator_trip
from gridlab.events import run_events

def test_trip_isolated_source_and_survivor_frequency_recovery():
    c = generator_trip()
    r = run_events(c.config, c.events, c.duration)
    assert abs(r.power[r.time >= 2, 1]).max() == 0
    assert r.power[-1, 0].real > .6
    assert abs(r.frequency_hz[-1, 0]-50) < .01
    assert np.isfinite(r.state).all()
