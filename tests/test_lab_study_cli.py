import json

from gridlab.cli import main


def test_sampled_delay_cli_saves_stability_results_and_provenance(tmp_path, capsys):
    out = tmp_path / "study.json"
    assert main(["lab", "study", "sample-delay", "--output", str(out)]) == 0
    data = json.loads(out.read_text())
    assert data["study"] == "sample-delay"
    assert any(not row["stable"] for row in data["results"])
    assert "git_commit" in data["provenance"]
