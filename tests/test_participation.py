import numpy as np
from gridlab.participation import participation

def test_decoupled_states_have_unit_participation():
    values, factors = participation(np.diag([-1., -3., -5.]))
    np.testing.assert_allclose(values, [-1, -3, -5])
    np.testing.assert_allclose(factors, np.eye(3))
