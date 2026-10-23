import numpy as np

from gridlab.converter.sensors import SampleDelay, SensorChain
from gridlab.converter.simulation import simulate_converter


def test_digital_measurement_and_one_sample_actuation_delay_recover_tracking():
    r = simulate_converter(
        duration=0.3, measurement=SensorChain(bits=12, noise_std=0.01), actuation_delay=SampleDelay(1, [0, 0])
    )
    assert r.command[0] == 0
    assert np.isfinite(r.state).all()
    assert abs(complex(*r.state[-1, 2:]) - 325) < 2
