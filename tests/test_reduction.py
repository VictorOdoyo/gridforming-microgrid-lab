import numpy as np

from gridlab.network import Line, admittance
from gridlab.reduction import kron_reduce


def test_series_lines_reduce_to_series_impedance():
    y = admittance(3, [Line(0, 1, 0.1, 0.2), Line(1, 2, 0.2, 0.3)])
    reduced = kron_reduce(y, [0, 2])
    expected = 1 / (0.3 + 0.5j) * np.array([[1, -1], [-1, 1]])
    np.testing.assert_allclose(reduced, expected)
