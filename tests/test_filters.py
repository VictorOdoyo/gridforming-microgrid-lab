import math

import pytest

from gridlab.filters import LowPass


def test_step_matches_analytical_solution_independent_of_partition():
    f = LowPass(0.2)
    for _ in range(100):
        f.step(3, 0.01)
    assert f.value == pytest.approx(3 * (1 - math.exp(-5)))
    assert f.step(0, 0) == f.value
