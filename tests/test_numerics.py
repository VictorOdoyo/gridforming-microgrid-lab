import numpy as np

from gridlab.numerics import rk4, ticks


def test_fourth_order_decay_and_exact_noninteger_endpoint():
    error = []
    for dt in (0.1, 0.05):
        x = np.array([1.0])
        for k in range(round(1 / dt)):
            x = rk4(lambda t, y: -y, k * dt, x, dt)
        error.append(abs(x[0] - np.exp(-1)))
    assert error[0] / error[1] > 15
    np.testing.assert_allclose(ticks(0.23, 0.1), [0, 0.1, 0.2, 0.23])
