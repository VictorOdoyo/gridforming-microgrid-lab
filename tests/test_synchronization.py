import numpy as np

from gridlab.synchronization import SyncCheck, phase_correction


def test_sync_guard_rejects_black_bus_and_large_mismatch():
    c = SyncCheck()
    assert c.accepts(1, 1, 50, 50)
    assert not c.accepts(0, 1, 50, 50)
    assert not c.accepts(np.exp(0.4j), 1, 50, 50)
    assert not c.accepts(1, 1, 49, 50)


def test_controller_chooses_shortest_phase_path():
    assert phase_correction(np.exp(-3j), np.exp(3j)) < 0
