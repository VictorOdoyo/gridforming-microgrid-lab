import numpy as np

from gridlab.converter.lc import LCPlant
from gridlab.converter.state_space import lc_state_space
from gridlab.discrete import zero_order_hold
from gridlab.numerics import rk4


def test_rk4_lc_step_agrees_with_independent_exact_linear_solution():
    p = LCPlant()
    a, b = lc_state_space(p, 0.1)
    ad, bd = zero_order_hold(a, b, 0.00001)
    exact = np.array([20.0, -2, 300, 5])
    numerical = exact.copy()
    command = 330 + 10j
    for k in range(100):
        exact = ad @ exact + bd @ [command.real, command.imag]
        numerical = rk4(lambda t, x: p.derivative(x, command, 0.1), k * 0.00001, numerical, 0.00001)
    np.testing.assert_allclose(numerical, exact, atol=2e-6)
