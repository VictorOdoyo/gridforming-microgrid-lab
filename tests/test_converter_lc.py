import numpy as np
import pytest

from gridlab.converter.lc import LCPlant


def test_lc_energy_derivative_matches_three_phase_power_balance():
    p = LCPlant()
    x = np.array([20, -3, 300, 10])
    u, g = 340 + 5j, 0.05
    dx = p.derivative(x, u, g)
    rate = 1.5 * (p.inductance_h * np.dot(x[:2], dx[:2]) + p.capacitance_f * np.dot(x[2:], dx[2:]))
    i, v = x[0] + 1j * x[1], x[2] + 1j * x[3]
    supply = 1.5 * (u * i.conjugate()).real
    loss = 1.5 * (p.resistance_ohm * abs(i) ** 2 + g * abs(v) ** 2)
    assert rate == pytest.approx(supply - loss)
