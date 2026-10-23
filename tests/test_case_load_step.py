import numpy as np
from gridlab.cases import load_step
from gridlab.events import run_events

def test_symmetric_inverters_share_the_disturbance_equally():
    case = load_step()
    r = run_events(case.config, case.events, duration=case.duration)
    np.testing.assert_allclose(r.power[:, 0], r.power[:, 1], atol=1e-10)
    assert r.frequency_hz[-1].mean() < 49.9
    assert np.max(r.network_residual) < 1e-10
