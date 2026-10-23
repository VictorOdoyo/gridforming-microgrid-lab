import numpy as np
import pytest
from gridlab.network import Line, admittance
from gridlab.powerflow import solve_powerflow

def test_resistive_two_bus_analytical_high_voltage_root():
    y = admittance(2, [Line(0, 1, .1, 0)])
    pf = solve_powerflow(y, [0, .5])
    expected = (1+np.sqrt(1-4*.1*.5))/2
    assert pf.voltage[1].real == pytest.approx(expected)
    assert pf.injection[1].real == pytest.approx(-.5)
    assert pf.mismatch < 1e-9
