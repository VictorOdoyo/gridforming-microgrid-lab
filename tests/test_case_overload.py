import numpy as np
from gridlab.cases import overload
from gridlab.events import run_events

def test_current_bound_is_maintained_at_cost_of_bus_voltage():
    c = overload()
    r = run_events(c.config, c.events, c.duration, sample_s=.05, max_step=.05)
    assert max(abs(r.current[:, 0])) <= .7+1e-8
    assert abs(r.voltage[-1, 0]) < .5
    assert max(r.network_residual) < 1e-8
