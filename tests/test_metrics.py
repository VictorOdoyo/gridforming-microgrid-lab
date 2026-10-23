import pytest
from gridlab.metrics import frequency_metrics

def test_linear_frequency_ramp_has_exact_rocof_and_area():
    m = frequency_metrics([0, 1, 2], [50, 49.5, 49])
    assert m["nadir_hz"] == 49
    assert m["max_abs_rocof_hz_s"] == .5
    assert m["integrated_absolute_error_hz_s"] == pytest.approx(1)
