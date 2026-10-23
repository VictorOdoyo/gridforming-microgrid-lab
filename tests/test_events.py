import numpy as np
import pytest

from gridlab.config import Inverter, Microgrid
from gridlab.events import Event, run_events


def case():
    return Microgrid(1, (), (0.4 + 0j,), (Inverter("a", 0, p_ref=0.4),))


def test_event_is_sampled_exactly_without_duplicate_times():
    r = run_events(case(), [Event(0.137, "load_scale", 2)], 0.4, 0.05)
    assert 0.137 in r.time
    assert np.all(np.diff(r.time) > 0)
    k = np.flatnonzero(r.time == 0.137)[0]
    assert r.power[k, 0].real > 1.5 * r.power[k - 1, 0].real


def test_final_time_event_is_right_continuous():
    r = run_events(case(), [Event(0.2, "load_scale", 0)], 0.2)
    assert abs(r.power[-1, 0]) < 1e-12


def test_out_of_horizon_event_rejected():
    with pytest.raises(ValueError):
        run_events(case(), [Event(2, "load_scale", 1)], 1)
