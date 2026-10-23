import numpy as np

from gridlab.config import Inverter, Microgrid
from gridlab.events import Event, run_events


def test_surviving_source_picks_up_tripped_generation():
    c = Microgrid(1, (), (0.6 + 0.1j,), (Inverter("a", 0), Inverter("b", 0)))
    r = run_events(c, [Event(0.2, "source_enabled", 0, 1)], 0.6)
    k = np.flatnonzero(r.time == 0.2)[0]
    assert abs(r.power[k:, 1]).max() == 0
    assert r.power[k, 0].real > 1.7 * r.power[k - 1, 0].real


def test_dispatch_event_changes_droop_frequency():
    c = Microgrid(1, (), (0.3 + 0j,), (Inverter("a", 0),))
    r = run_events(c, [Event(0.2, "p_ref", 0.5)], 0.3)
    k = np.flatnonzero(r.time == 0.2)[0]
    assert r.frequency_hz[k, 0] - r.frequency_hz[k - 1, 0] > 0.19
