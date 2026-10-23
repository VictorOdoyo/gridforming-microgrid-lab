import numpy as np

from gridlab.converter.simulation import simulate_converter


def test_dc_sag_limits_available_voltage_and_control_recovers_without_persistent_windup():
    r = simulate_converter(
        duration=0.35, conductance=lambda t: 0.1, dc_voltage=lambda t: 450 if 0.08 <= t < 0.15 else 700
    )
    v = r.state[:, 2] + 1j * r.state[:, 3]
    during = (r.time >= 0.1) & (r.time < 0.15)
    assert np.mean(abs(v[during])) < 300
    assert np.max(abs(r.command) - r.dc_voltage / np.sqrt(3)) < 1e-9
    assert abs(v[-1] - 325) < 1
