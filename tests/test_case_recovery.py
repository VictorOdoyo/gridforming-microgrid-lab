import numpy as np
from gridlab.cases import island_recovery
from gridlab.events import run_events

def test_outage_recovery_passes_reclose_guard():
    c = island_recovery()
    r = run_events(c.config, c.events, c.duration, sample_s=.05, max_step=.05)
    assert np.all(np.isfinite(r.state))
    assert abs(r.frequency_hz[-1, 0]-50) < .02
    assert abs(np.angle(r.voltage[r.time == 16, 0][0])) < .2
