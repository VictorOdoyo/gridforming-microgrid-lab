import numpy as np

from gridlab.converter.lc import LCPlant
from gridlab.converter.state_space import lc_state_space, steady_state


def test_analytical_matrix_matches_physical_equations_and_equilibrium():
    p = LCPlant()
    a, b = lc_state_space(p, 0.1)
    x, u = np.array([1.0, 2, 300, -10]), 330 + 20j
    np.testing.assert_allclose(p.derivative(x, u, 0.1), a @ x + b @ [u.real, u.imag])
    eq = steady_state(p, u, 0.1)
    np.testing.assert_allclose(p.derivative(eq, u, 0.1), 0, atol=1e-9)
