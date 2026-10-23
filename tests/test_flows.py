import pytest
from gridlab.network import Line, admittance
from gridlab.norton import solve_network
from gridlab.flows import branch_flow, balance_error

def test_power_balance_matches_i_squared_r():
    line = Line(0, 1, .02, .1)
    y = admittance(2, [line], [0, .5-.2j])
    p = solve_network(y, [0], [.05j], [1])
    flow = branch_flow(line, p.voltage)
    assert flow.loss.real == pytest.approx(abs(flow.series_current)**2*.02)
    load = abs(p.voltage[1])**2*(.5+.2j)
    assert abs(balance_error(p.power, [load], [line], p.voltage)) < 1e-12
