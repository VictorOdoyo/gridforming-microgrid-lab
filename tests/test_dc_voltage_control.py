import pytest

from gridlab.dc.voltage_control import DCVoltageControl


def test_dc_current_feedforward_and_voltage_support():
    c = DCVoltageControl()
    assert c.step(700, 600, 60000, 0.001) == pytest.approx(100)
    assert c.step(690, 600, 60000, 0.001) > 100
    assert c.step(0, 600, 0, 0.001) == 200
