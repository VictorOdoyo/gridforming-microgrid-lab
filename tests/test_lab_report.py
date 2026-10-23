import hashlib
import json

from gridlab.dc.system import DCSystem
from gridlab.lab.case import LabCase, run_case
from gridlab.lab.report import write_report


def test_physical_report_authenticates_saved_data_and_preserves_case(tmp_path):
    c = LabCase("physical", "dc", "DC validation", DCSystem(), 0.002)
    metrics = write_report(c, run_case(c), tmp_path)
    for name, digest in json.loads((tmp_path / "manifest.json").read_text()).items():
        assert hashlib.sha256((tmp_path / name).read_bytes()).hexdigest() == digest
    assert metrics["kind"] == "dc"
    assert json.loads((tmp_path / "provenance.json").read_text())["period_s"] == 0.00005
