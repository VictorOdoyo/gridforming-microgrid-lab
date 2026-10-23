import numpy as np

from gridlab.converter.active_damping import damping_command, default_lcl, lcl_matrix


def test_active_damping_moves_oscillatory_lcl_poles_left():
    p = default_lcl()
    without = np.linalg.eigvals(lcl_matrix(p))
    with_damping = np.linalg.eigvals(lcl_matrix(p, 2))
    oscillatory_without = without[abs(without.imag) > 1]
    oscillatory_with = with_damping[abs(with_damping.imag) > 1]
    assert oscillatory_with.real.max() < oscillatory_without.real.max()
    assert damping_command(300, 20, 10, 2) == 280
