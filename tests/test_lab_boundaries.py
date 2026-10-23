import numpy as np

from gridlab.converter.simulation import simulate_converter
from gridlab.dc.simulation import simulate_dc
from gridlab.hybrid.simulation import simulate_hybrid


def test_all_physical_drivers_sample_noninteger_signal_boundaries():
    for simulate in (simulate_dc, simulate_converter, simulate_hybrid):
        r = simulate(duration=0.002, boundaries=(0.001025,))
        assert 0.001025 in r.time
        assert np.all(np.diff(r.time) > 0)
