import numpy as np
import pytest

from gridlab.hybrid.plant import HybridPlant


def test_ac_and_dc_exchange_exactly_the_same_inverter_power():
    p = HybridPlant()
    x = p.initial()
    x[2], x[1], x[5:9] = 100, 2, [20, -2, 300, 5]
    duty, command, g = 0.8, 340 + 10j, 0.1
    obs = p.observe(x, duty, command)
    dx = p.derivative(0, x, duty, command, g)
    storage_rate = (
        dx[3]
        + p.dc.converter.inductance_h * x[2] * dx[2]
        + p.dc.polarization.capacitance_f * x[1] * dx[1]
        + 1.5 * p.ac.inductance_h * np.dot(x[5:7], dx[5:7])
        + 1.5 * p.ac.capacitance_f * np.dot(x[7:9], dx[7:9])
    )
    passive = 1.5 * (p.ac.resistance_ohm * np.dot(x[5:7], x[5:7]) + g * np.dot(x[7:9], x[7:9]))
    expected = obs["chemical_w"] - obs["heat_w"] - obs["inverter_loss_w"] - passive
    assert storage_rate == pytest.approx(expected, abs=1e-7)
