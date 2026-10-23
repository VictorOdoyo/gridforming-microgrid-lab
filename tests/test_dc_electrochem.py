import pytest

from gridlab.dc.electrochem import Polarization, soc_derivative


def test_one_hour_capacity_current_exhausts_one_soc_unit():
    assert soc_derivative(200, 200) * 3600 == -1
    assert soc_derivative(-200, 200) * 3600 == pytest.approx(0.995)


def test_rc_power_splits_into_storage_and_dissipation():
    p = Polarization()
    vp, current = 3, 150
    stored_rate = p.capacitance_f * vp * p.derivative(vp, current)
    assert vp * current == pytest.approx(stored_rate + vp**2 / p.resistance_ohm)
