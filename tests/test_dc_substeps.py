import numpy as np

from gridlab.dc.simulation import simulate_dc


def test_more_plant_substeps_preserve_control_ticks_and_total_horizon():
    a = simulate_dc(duration=0.01, integration_substeps=1)
    b = simulate_dc(duration=0.01, integration_substeps=4)
    np.testing.assert_array_equal(a.time, b.time)
    assert abs(a.state[-1, 3] - b.state[-1, 3]) < 0.1
