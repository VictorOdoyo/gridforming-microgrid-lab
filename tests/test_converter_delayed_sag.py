import numpy as np

from gridlab.converter.sensors import SampleDelay
from gridlab.converter.simulation import simulate_converter


def test_delayed_command_is_relimited_using_current_dc_supply():
    r = simulate_converter(
        duration=0.03, dc_voltage=lambda t: 450 if t >= 0.02 else 700, actuation_delay=SampleDelay(1, [0, 0])
    )
    assert np.max(abs(r.command) - r.dc_voltage / np.sqrt(3)) < 1e-9
