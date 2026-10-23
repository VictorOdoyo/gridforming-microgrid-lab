import pytest

from gridlab.dc.bus import Bus


def test_energy_based_brownout_prediction():
    b = Bus()
    e = b.energy(700)
    seconds = b.time_to_brownout(e, 10000)
    assert b.voltage(e - 10000 * seconds) == pytest.approx(450)
    assert b.time_to_brownout(e, 0) == float("inf")
