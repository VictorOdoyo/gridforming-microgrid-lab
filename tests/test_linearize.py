import numpy as np

from gridlab.linearize import jacobian


def test_jacobian_matches_analytical_nonlinear_derivatives():
    x = np.array([0.7, -0.2])
    j = jacobian(lambda a: [a[0] ** 2 + a[1], np.sin(a[0]) * a[1]], x)
    expected = [[1.4, 1], [np.cos(0.7) * (-0.2), np.sin(0.7)]]
    np.testing.assert_allclose(j, expected, atol=1e-9)
