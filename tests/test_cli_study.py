import json

from gridlab.cli import main


def test_daily_energy_study_writes_complete_json(tmp_path, capsys):
    target = tmp_path / "study.json"
    assert main(["study", "daily-energy", "--output", str(target)]) == 0
    report = json.loads(target.read_text())
    assert report["summary"]["unmet_kwh"] == 0
    assert json.loads(capsys.readouterr().out)["study"] == "daily-energy"
