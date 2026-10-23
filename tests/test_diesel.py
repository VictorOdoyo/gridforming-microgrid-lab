from gridlab.diesel import DieselGovernor

def test_ramp_and_steady_state_limits():
    g = DieselGovernor(100, .5, 10, 20)
    assert g.derivative(0, 100) == 10
    assert g.derivative(100, 500) == 0
    assert g.derivative(40, 40) == 0
    assert g.derivative(40, 40, enabled=False) == -10
