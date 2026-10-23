import numpy as np
import pytest

from gridlab.dc.system import DCSystem


@pytest.mark.parametrize("closed", [True, False])
def test_coupled_dc_plant_satisfies_instantaneous_energy_conservation(closed):
    s = DCSystem()
    x = s.initial(current_a=100)
    x[1] = 3
    duty, load = 0.8, 50000
    p = s.observe(x, duty, closed)
    dx = s.derivative(0, x, duty, load, closed)
    stored_rate = (
        dx[3] + s.converter.inductance_h * x[2] * dx[2] + s.polarization.capacitance_f * x[1] * dx[1]
    )
    assert p["chemical_w"] - load - p["heat_w"] == pytest.approx(stored_rate, abs=1e-8)
    assert np.isfinite(dx).all()
