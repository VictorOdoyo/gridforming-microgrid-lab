import pytest

from gridlab.dc.pack import Pack


def test_ocv_interpolation_and_temperature_resistance():
    p = Pack()
    assert p.ocv(0.3) == pytest.approx(590)
    assert p.resistance(0) > p.resistance(25)
    with pytest.raises(ValueError):
        p.ocv(1.1)
