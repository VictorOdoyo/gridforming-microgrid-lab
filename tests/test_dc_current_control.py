import pytest

from gridlab.dc.current_control import DCCurrentControl


def test_current_error_selects_correct_halfbridge_direction():
    c = DCCurrentControl()
    idle = c.step(0, 0, 600, 700, 0.05, 0.001)
    increase = c.step(100, 0, 600, 700, 0.05, 0.001)
    assert idle == pytest.approx(600 / 700)
    assert increase < idle
    for _ in range(100):
        assert c.step(1e6, 0, 600, 700, 0.05, 0.001) == 0
    assert abs(c.integral_v) < 100
