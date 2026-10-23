import numpy as np

from gridlab.converter.switching import bridge_states, phase_voltages


def test_carrier_average_matches_duty_and_floating_neutral_kcl():
    t = (np.arange(10000) + 0.5) / 10000 / 10000
    duty = np.array([0.2, 0.5, 0.8])
    states = bridge_states(t, duty, 10000)
    np.testing.assert_allclose(states.mean(axis=0), duty, atol=1e-4)
    voltage = phase_voltages(states, 700)
    np.testing.assert_allclose(voltage.sum(axis=1), 0, atol=1e-12)
