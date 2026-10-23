import numpy as np

from gridlab.transformer import Transformer


def test_open_circuit_voltage_follows_complex_tap():
    a = 1.1 * np.exp(0.1j)
    y = Transformer(0, 1, 0.1j, 1.1, 0.1).stamp(np.zeros((2, 2)))
    np.testing.assert_allclose(y @ [a, 1], 0, atol=1e-14)


def test_passive_real_power():
    y = Transformer(0, 1, 0.01 + 0.1j, 1.05, 0.05).stamp(np.zeros((2, 2)))
    v = np.array([1, 0.95 * np.exp(-0.1j)])
    assert np.sum(v * np.conj(y @ v)).real > 0
