import numpy as np
from gridlab.config import Microgrid, Inverter
from gridlab.events import Event, run_events

def test_every_record_satisfies_nodal_kcl():
    c = Microgrid(1, (), (.5+.2j,), (Inverter("a", 0),))
    r = run_events(c, [Event(.1, "load_scale", 2)], .2)
    assert max(r.network_residual) < 1e-10
    for k, t in enumerate(r.time):
        scale = 1 if t < .1 else 2
        np.testing.assert_allclose(r.current[k, 0], (.5-.2j)*scale*r.voltage[k, 0], atol=1e-10)
