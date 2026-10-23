import numpy as np
import pytest

from gridlab.dc.control import DCControl
from gridlab.dc.system import DCSystem
from gridlab.hybrid.audit import audit_hybrid
from gridlab.hybrid.events import HybridEvent
from gridlab.hybrid.plant import HybridPlant
from gridlab.hybrid.simulation import simulate_hybrid


def test_precharge_resistor_current_and_whole_dc_energy_identity():
    s = DCSystem()
    x = s.initial(voltage=450)
    p = s.observe(x, 0, closed=False, precharge=True)
    dx = s.derivative(0, x, 0, 0, closed=False, precharge=True)
    assert 0 < p["battery_current_a"] < 100
    storage = dx[3] + s.polarization.capacitance_f * x[1] * dx[1]
    assert p["chemical_w"] - p["heat_w"] == pytest.approx(storage)
    c = DCControl()
    _, closed = c.step(s, x, 0, 0.0001, reset=True)
    assert not closed and c.precharging


def test_rearm_uses_precharge_and_avoids_previous_boost_inrush():
    r = simulate_hybrid(
        duration=0.9,
        period_s=0.0001,
        events=(
            HybridEvent(0.1, "battery-trip"),
            HybridEvent(0.4, "battery-reset"),
            HybridEvent(0.4, "gate-reset"),
        ),
    )
    assert r.precharge.any()
    assert not (r.precharge & r.closed).any()
    assert r.closed[-1] and r.gate[-1]
    assert np.max(abs(r.state[:, 2])) < 250
    assert audit_hybrid(HybridPlant(), r)["relative_residual"] < 1e-3
