import pytest

from gridlab.cases import load_step
from gridlab.events import run_events
from gridlab.report import write_report
from gridlab.storage import load_result, save_result


def test_solver_settings_survive_saved_trace_roundtrip(tmp_path):
    c = load_step()
    r = run_events(c.config, (), 0.1, sample_s=0.03, max_step=0.01, rtol=1e-6)
    save_result(r, tmp_path / "trace.npz")
    loaded = load_result(tmp_path / "trace.npz")
    assert loaded.solver_options["sample_s"] == 0.03
    assert loaded.solver_options["rtol"] == 1e-6
    with pytest.raises(ValueError, match="duration"):
        write_report(c, r, tmp_path / "bad-report")
