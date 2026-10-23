import numpy as np

from gridlab.dc.audit import audit_dc
from gridlab.dc.events import DCEvent
from gridlab.dc.simulation import simulate_dc
from gridlab.dc.system import DCSystem


def test_trip_preserves_continuous_plant_state_and_reset_recovers_supply():
    p = DCSystem()
    r = simulate_dc(p, duration=0.15, events=(DCEvent(0.05, "trip"), DCEvent(0.06, "reset")))
    off = (r.time >= 0.05) & (r.time < 0.06)
    assert not r.closed[off].any()
    assert r.closed[r.time >= 0.06].all()
    k = np.flatnonzero(r.time == 0.05)[0]
    assert abs(r.state[k, 2]) > 1
    assert r.termination == "completed"
    assert audit_dc(p, r)["relative_residual"] < 1e-4
