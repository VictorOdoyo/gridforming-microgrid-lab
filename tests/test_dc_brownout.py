from gridlab.dc.control import DCControl
from gridlab.dc.simulation import simulate_dc
from gridlab.dc.system import DCSystem


def test_open_battery_causes_predictable_capacitor_brownout():
    system = DCSystem()
    state = system.initial(soc=0.09)
    expected = system.bus.time_to_brownout(state[3], 50000)
    r = simulate_dc(system, lambda t: 50000, 0.2, initial=state, control=DCControl())
    assert r.termination == "undervoltage"
    assert abs(r.time[-1] - expected) <= 0.00011
    assert not r.closed.any()
    assert r.state[-1, 0] == 0.09
