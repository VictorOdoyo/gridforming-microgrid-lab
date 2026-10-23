import numpy as np

from gridlab.hybrid.events import HybridEvent
from gridlab.hybrid.simulation import simulate_hybrid


def test_battery_and_gate_rearm_recover_the_complete_power_path():
    events = (
        HybridEvent(0.1, "battery-trip"),
        HybridEvent(0.4, "battery-reset"),
        HybridEvent(0.4, "gate-reset"),
    )
    r = simulate_hybrid(duration=0.9, events=events)
    assert (~r.gate).any()
    assert r.closed[-1] and r.gate[-1]
    assert abs(complex(*r.state[-1, 7:9]) - 325) < 3
    assert np.sqrt(2 * r.state[-1, 3] / 0.05) > 690
