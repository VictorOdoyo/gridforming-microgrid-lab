import hashlib
import json
from dataclasses import replace

from gridlab.cases import load_step
from gridlab.events import run_events
from gridlab.report import write_report


def test_report_manifest_authenticates_every_delivered_file(tmp_path):
    case = replace(load_step(), duration=0.2, events=())
    r = run_events(case.config, (), 0.2)
    metrics = write_report(case, r, tmp_path)
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    for name, checksum in manifest.items():
        assert hashlib.sha256((tmp_path / name).read_bytes()).hexdigest() == checksum
    assert metrics["maximum_network_residual"] < 1e-9
    assert "<table>" in (tmp_path / "index.html").read_text()
