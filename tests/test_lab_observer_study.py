from gridlab.lab.observer_study import observer_study


def test_seeded_observer_recovers_currents_from_noisy_voltage_only():
    a = observer_study(17)
    assert a == observer_study(17)
    assert a["current_d_rms_error_a"] < 1
    assert a["current_q_rms_error_a"] < 1
    assert a["minimum_covariance_eigenvalue"] >= 0
