import numpy as np

from gridlab.lcl import LCLFilter


def test_unforced_lossless_energy_derivative_is_zero():
    f = LCLFilter(0.001, 0.002, 20e-6)
    x = np.array([2 + 1j, 10 + 3j, 1 - 1j])
    dx = f.derivative(x, 0, 0)
    rate = np.real(np.vdot(x, np.array([f.l1, f.capacitance, f.l2]) * dx))
    assert abs(rate) < 1e-10
    assert 1000 < f.resonance_hz < 1500
