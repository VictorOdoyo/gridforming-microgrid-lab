import numpy as np

from gridlab.config import Inverter, Microgrid
from gridlab.simulation import simulate
from gridlab.storage import load_result, save_result


def test_archive_roundtrip_preserves_complex_arrays(tmp_path):
    r = simulate(Microgrid(1, (), (0.3 + 0.1j,), (Inverter("a", 0),)), 0.1)
    path = tmp_path / "run.npz"
    save_result(r, path)
    loaded = load_result(path)
    assert loaded.source_names == r.source_names
    for name in ("time", "state", "voltage", "power", "enabled", "current"):
        np.testing.assert_array_equal(getattr(r, name), getattr(loaded, name))
