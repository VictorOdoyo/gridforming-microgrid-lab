from gridlab.integration_study import integration_study


def test_event_simulation_agrees_with_tight_reference():
    rows = integration_study((0.05,), 2.3)
    assert rows[0]["frequency_error"]["max_abs"] < 1e-3
    assert rows[0]["state_error"]["max_abs"] < 1e-3
