import numpy as np

from gridlab.config import Inverter, Microgrid
from gridlab.events import Event, run_events
from gridlab.network import Line


def test_open_tie_separates_frequency_responses():
    c = Microgrid(
        2,
        (Line(0, 1, 0.02, 0.1),),
        (0.2 + 0j, 0.6 + 0j),
        (Inverter("a", 0, p_ref=0.4), Inverter("b", 1, p_ref=0.4)),
    )
    r = run_events(c, [Event(0.5, "line_enabled", 0)], 3)
    assert r.frequency_hz[-1, 0] > r.frequency_hz[-1, 1] + 0.2
    assert np.isfinite(r.state).all()
