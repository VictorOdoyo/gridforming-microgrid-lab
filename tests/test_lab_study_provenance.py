import hashlib
import json

from gridlab.cli import main


def test_study_hash_authenticates_actual_saved_model_and_experiment_axes(tmp_path, capsys):
    path = tmp_path / "study.json"
    main(["lab", "study", "sample-delay", "--output", str(path)])
    data = json.loads(path.read_text())
    canonical = json.dumps(data["configuration"], sort_keys=True, separators=(",", ":"), allow_nan=False)
    assert hashlib.sha256(canonical.encode()).hexdigest() == data["provenance"]["configuration_sha256"]
    assert data["configuration"]["parameters"]["delay_samples"] == [0, 1, 2]
