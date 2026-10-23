import pytest

from gridlab.droop import Droop


def test_load_increase_reduces_frequency_and_voltage():
    d = Droop(2, 0.1)
    assert d.frequency(0.7, 0.5) == pytest.approx(49.6)
    assert d.voltage(0.3, 0.1) == pytest.approx(0.98)
    assert d.frequency(0.7, 0.5, 0.4) == pytest.approx(50)
