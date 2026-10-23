import numpy as np

from gridlab.cases import black_start
from gridlab.events import run_events


def test_staged_black_start_energizes_bus_and_recovers():
    c = black_start()
    r = run_events(c.config, c.events, c.duration)
    assert r.voltage[0, 0] == 0
    assert abs(r.voltage[-1, 0]) > 0.9
    assert abs(r.frequency_hz[-1].mean() - 50) < 0.01
    assert np.max(abs(r.current)) < 1
