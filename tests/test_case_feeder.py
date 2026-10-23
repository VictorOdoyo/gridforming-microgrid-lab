import numpy as np
from gridlab.cases import radial_feeder
from gridlab.events import run_events
from gridlab.flows import balance_error

def test_feeder_maintains_global_power_balance_after_load_step():
    c = radial_feeder()
    r = run_events(c.config, c.events, c.duration, sample_s=.05, max_step=.05)
    demand = np.array(c.config.loads)*[1, 1.5, 1]*abs(r.voltage[-1])**2
    assert abs(balance_error(r.power[-1], demand, c.config.lines, r.voltage[-1])) < 1e-9
    assert np.ptp(r.frequency_hz[-1]) < .001
    assert np.ptp(abs(r.voltage[-1])) > .001
