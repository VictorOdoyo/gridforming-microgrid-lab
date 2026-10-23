import numpy as np

from gridlab.converter.lc import LCPlant
from gridlab.converter.lqr import lqr_gain, voltage_equilibrium
from gridlab.converter.state_space import lc_state_space


def test_riccati_identity_and_closed_loop_stability():
    plant = LCPlant()
    a, b = lc_state_space(plant, 0.1)
    k, p = lqr_gain(plant, 0.1)
    residual = a.T @ p + p @ a - p @ b @ np.linalg.solve(np.eye(2) * 0.1, b.T @ p) + np.diag([1, 1, 10, 10])
    assert np.linalg.norm(residual) < 1e-5
    assert np.linalg.eigvals(a - b @ k).real.max() < 0
    x, u = voltage_equilibrium(plant, 0.1, 325 + 0j)
    np.testing.assert_allclose(plant.derivative(x, u, 0.1), 0, atol=1e-8)
