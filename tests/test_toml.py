from pathlib import Path
from gridlab.config_io import load_case
from gridlab.events import run_events

def test_bundled_toml_is_executable():
    path = Path(__file__).parents[1]/"examples"/"custom-island.toml"
    c = load_case(path)
    r = run_events(c.config, c.events, 3, sample_s=.1, max_step=.05)
    assert len(r.source_names) == 2
    assert r.time[-1] == 3
