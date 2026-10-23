from gridlab.cases import load_step
from gridlab.stability import stability_report


def test_gauge_and_unused_droop_states_are_removed():
    report = stability_report(load_step().config)
    assert 0 not in report["state_indices"]
    assert 1 not in report["state_indices"]
    assert 6 not in report["state_indices"]
    assert report["spectral_abscissa"] < 0
    assert all(m["classification"] == "stable" for m in report["modes"])
