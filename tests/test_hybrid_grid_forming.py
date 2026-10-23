import pytest

from gridlab.hybrid.grid_forming import GridForming


def test_swing_rocof_and_primary_droop_equilibrium_on_shared_power_base():
    g = GridForming()
    dx = g.derivative([0, 0, 0.5, 0], 50000, 50)
    assert dx[1] == pytest.approx(-2.5)
    assert dx[2] == 0
    equilibrium = [0, -0.2, 0.5, 0]
    assert g.derivative(equilibrium, 50000, 50)[1] == pytest.approx(0)
    assert GridForming(mode="droop").deviation(equilibrium) == pytest.approx(-0.2)
