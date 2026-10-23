import numpy as np

from gridlab.converter.sensors import SampleDelay, SensorChain


def test_delay_is_exact_and_seeded_measurements_are_reproducible():
    delay = SampleDelay(2, [0])
    assert delay.step([1])[0] == 0
    assert delay.step([2])[0] == 0
    assert delay.step([3])[0] == 1
    a, b = SensorChain(noise_std=0.1), SensorChain(noise_std=0.1)
    for _ in range(5):
        np.testing.assert_array_equal(a([1, 2, 300, 0]), b([1, 2, 300, 0]))
