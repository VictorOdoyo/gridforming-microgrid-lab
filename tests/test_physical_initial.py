import pytest

from gridlab.converter.simulation import simulate_converter
from gridlab.dc.simulation import simulate_dc
from gridlab.dc.system import DCSystem
from gridlab.hybrid.simulation import simulate_hybrid
from gridlab.numerics import ticks


@pytest.mark.parametrize("solver", [simulate_dc, simulate_converter, simulate_hybrid])
def test_invalid_initial_state_is_rejected_clearly(solver):
    with pytest.raises(ValueError, match="initial"):
        solver(duration=0.001, initial=[float("nan")])


def test_zero_initial_dc_voltage_is_not_replaced_silently():
    assert DCSystem().initial(voltage=0)[3] == 0
    with pytest.raises(ValueError):
        ticks(1, 1e-12)
