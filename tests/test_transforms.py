import numpy as np
from gridlab.transforms import clarke, inverse_clarke, park, inverse_park

def test_balanced_phases_become_constant_d_axis():
    t = np.linspace(0, 2*np.pi, 101)
    abc = np.cos(t[:, None] + np.array([0, -2*np.pi/3, 2*np.pi/3]))
    dq = park(clarke(abc), t)
    np.testing.assert_allclose(dq, np.tile([1, 0, 0], (101, 1)), atol=1e-14)

def test_roundtrip_with_zero_sequence():
    x = np.random.default_rng(2).normal(size=(20, 3))
    np.testing.assert_allclose(inverse_clarke(inverse_park(park(clarke(x), .4), .4)), x)
