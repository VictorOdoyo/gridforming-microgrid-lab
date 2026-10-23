from gridlab.protection.gate import GateSupervisor


def test_voltage_hysteresis_dwell_and_explicit_reset():
    g = GateSupervisor(dwell_s=0.02)
    assert not g.step(440, 25, 0.01)
    assert not g.step(600, 25, 0.01, reset=True)
    assert not g.step(700, 25, 0.01)
    assert g.step(700, 25, 0.01)
    assert not g.step(700, 80, 0.01)
    assert not g.step(700, 60, 0.1, reset=True)
    assert g.step(700, 50, 0.1)
