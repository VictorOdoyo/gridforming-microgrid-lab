import numpy as np
from gridlab.discrete import zero_order_hold, schur_stable

def test_exact_first_order_sample_and_integrator():
    a, b = zero_order_hold([[-2]], [[2]], .1)
    np.testing.assert_allclose(a, [[np.exp(-.2)]])
    np.testing.assert_allclose(b, [[1-np.exp(-.2)]])
    assert schur_stable(a)
    assert not schur_stable([[1]])
