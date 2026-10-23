import pytest
from gridlab.thevenin import TheveninCell

def test_dc_pulse_approaches_total_series_resistance():
    c = TheveninCell(.01, .02, 100)
    vp, voltage = c.step(0, 10, .5, 100)
    assert vp == pytest.approx(.2)
    assert voltage == pytest.approx(3.6-.3)

def test_rest_relaxes_polarization():
    c = TheveninCell(.01, .02, 100)
    vp, _ = c.step(.2, 0, .5, 2)
    assert vp == pytest.approx(.2/2.718281828459045)
