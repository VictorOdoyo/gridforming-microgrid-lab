import pytest
from gridlab.droop import Droop

def test_load_increase_reduces_frequency_and_voltage():
    d = Droop(2, .1)
    assert d.frequency(.7, .5) == pytest.approx(49.6)
    assert d.voltage(.3, .1) == pytest.approx(.98)
    assert d.frequency(.7, .5, .4) == pytest.approx(50)
