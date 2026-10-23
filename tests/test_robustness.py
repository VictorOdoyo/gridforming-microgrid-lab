from gridlab.robustness import robustness_study

def test_seeded_uncertainty_keeps_parameters_and_failure_count():
    report = robustness_study(3, 17)
    assert len(report["trials"]) == 3
    assert report["failed_trials"] == 0
    assert report["seed"] == 17
    assert 47 < report["nadir_percentiles_hz"][50] < 50
    assert all("load_factor" in t.parameters for t in report["trials"])
