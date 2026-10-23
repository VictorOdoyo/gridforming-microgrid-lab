from dataclasses import replace

import numpy as np
import pytest

from gridlab.dc.simulation import simulate_dc
from gridlab.lab.storage import load_trace, save_trace


def test_physical_archive_roundtrip_and_nonfinite_rejection(tmp_path):
    r = simulate_dc(duration=0.002)
    path = tmp_path / "trace.npz"
    save_trace("dc", r, path, {"period_s": 0.0001})
    kind, loaded, meta = load_trace(path)
    assert kind == "dc" and meta["period_s"] == 0.0001
    np.testing.assert_array_equal(loaded.state, r.state)
    bad = r.state.copy()
    bad[0, 0] = np.nan
    with pytest.raises(ValueError):
        save_trace("dc", replace(r, state=bad), tmp_path / "bad.npz")
