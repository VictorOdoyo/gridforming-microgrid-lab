import numpy as np
import pytest

from gridlab.lyapunov import lyapunov_certificate


def test_certificate_satisfies_energy_decay_identity():
    a = np.array([[-2.0, 1], [0, -1.0]])
    p = lyapunov_certificate(a)
    np.testing.assert_allclose(a.T @ p + p @ a, -np.eye(2), atol=1e-12)
    with pytest.raises(ValueError):
        lyapunov_certificate([[0]])
