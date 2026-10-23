import numpy as np

from gridlab.numerics import rk4_substeps


def test_substeps_resolve_fast_passive_decay_inside_a_held_control_interval():
    x = rk4_substeps(lambda t, y: -100000 * y, 0, [1.0], 0.00005, 20)
    np.testing.assert_allclose(x, [np.exp(-5)], rtol=3e-4)
