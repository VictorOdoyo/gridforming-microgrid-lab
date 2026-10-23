import pytest

from gridlab.quality import sharing_error, voltage_metrics


def test_constant_sag_duration_and_proportional_sharing():
    m = voltage_metrics([0, 1, 2], [0.8, 0.8, 0.8])
    assert m["outside_band_bus_seconds"] == 2
    assert sharing_error([0.6, 0.3], [2, 1]) == pytest.approx(0)
    assert sharing_error([0.6, 0.6], [2, 1]) > 0
