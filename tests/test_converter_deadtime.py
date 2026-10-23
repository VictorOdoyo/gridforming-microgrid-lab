import pytest

from gridlab.converter.deadtime import compensate_deadtime, deadtime_error


def test_deadtime_error_opposes_current_and_compensation_cancels_it():
    current = [10, -5, -5]
    error = deadtime_error(current, 700, 2e-6, 10000)
    assert error.real < 0
    assert deadtime_error([-x for x in current], 700, 2e-6, 10000) == pytest.approx(-error)
    assert compensate_deadtime(300, current, 700, 2e-6, 10000) + error == pytest.approx(300)
