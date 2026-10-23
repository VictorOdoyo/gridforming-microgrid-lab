import pytest
from gridlab.quality import voltage_metrics, sharing_error

def test_constant_sag_duration_and_proportional_sharing():
    m = voltage_metrics([0, 1, 2], [.8, .8, .8])
    assert m["outside_band_bus_seconds"] == 2
    assert sharing_error([.6, .3], [2, 1]) == pytest.approx(0)
    assert sharing_error([.6, .6], [2, 1]) > 0
