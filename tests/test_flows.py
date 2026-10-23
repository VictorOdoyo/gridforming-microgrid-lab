import pytest

from gridlab.flows import balance_error, branch_flow
from gridlab.network import Line, admittance
from gridlab.norton import solve_network


def test_power_balance_matches_i_squared_r():
    line = Line(0, 1, 0.02, 0.1)
    y = admittance(2, [line], [0, 0.5 - 0.2j])
    p = solve_network(y, [0], [0.05j], [1])
    flow = branch_flow(line, p.voltage)
    assert flow.loss.real == pytest.approx(abs(flow.series_current) ** 2 * 0.02)
    load = abs(p.voltage[1]) ** 2 * (0.5 + 0.2j)
    assert abs(balance_error(p.power, [load], [line], p.voltage)) < 1e-12
