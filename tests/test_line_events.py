import numpy as np
from gridlab.config import Microgrid, Inverter
from gridlab.network import Line
from gridlab.events import Event, run_events

def test_open_tie_separates_frequency_responses():
    c = Microgrid(2, (Line(0, 1, .02, .1),), (.2+0j, .6+0j),
                  (Inverter("a", 0, p_ref=.4), Inverter("b", 1, p_ref=.4)))
    r = run_events(c, [Event(.5, "line_enabled", 0)], 3)
    assert r.frequency_hz[-1, 0] > r.frequency_hz[-1, 1]+.2
    assert np.isfinite(r.state).all()
