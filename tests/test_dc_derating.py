import pytest

from gridlab.dc.derating import Envelope


def test_soc_and_thermal_envelopes_reduce_available_current():
    e = Envelope()
    assert e.constrain(200, 0.1, 25) == 0
    assert e.constrain(-100, 0.9, 25) == 0
    assert e.constrain(200, 0.125, 25) == pytest.approx(100)
    assert e.constrain(200, 0.5, 52.5) == pytest.approx(100)
    assert e.constrain(200, 0.5, 60) == 0
