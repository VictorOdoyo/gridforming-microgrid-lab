import numpy as np

from gridlab.converter.simulation import simulate_converter


def test_inner_loops_establish_voltage_and_recover_after_load_step():
    r = simulate_converter()
    voltage = r.state[:, 2] + 1j * r.state[:, 3]
    assert abs(voltage[-1] - 325) < 0.5
    assert abs(voltage[r.time > 0.2] - 325).max() < 5
    assert np.isfinite(r.state).all()
    assert np.max(abs(r.command)) <= 700 / np.sqrt(3) + 1e-9
