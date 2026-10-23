import pytest

from gridlab.dc.chemical import chemical_capacity_kwh, chemical_energy
from gridlab.dc.pack import Pack


def test_linear_ocv_integral_and_local_energy_derivative():
    p = Pack(100, (0, 1), (500, 700))
    assert chemical_capacity_kwh(p) == pytest.approx(60)
    assert chemical_energy(p, 0.5) / 3_600_000 == pytest.approx(27.5)
    h = 1e-6
    derivative = (chemical_energy(p, 0.4 + h) - chemical_energy(p, 0.4 - h)) / (2 * h)
    assert derivative == pytest.approx(p.ocv(0.4) * 100 * 3600, rel=1e-8)
