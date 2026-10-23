from gridlab.comparison import compare_controls

def test_both_controls_reach_same_steady_droop_relationship():
    result = compare_controls(duration=6)
    droop = result["droop"]["trace"]
    vsm = result["vsm"]["trace"]
    assert abs(droop.frequency_hz[-1].mean()-vsm.frequency_hz[-1].mean()) < .005
    assert result["droop"]["metrics"]["nadir_hz"] < 50
    assert result["vsm"]["metrics"]["nadir_hz"] < 50
