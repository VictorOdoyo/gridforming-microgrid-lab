import json
import pytest
from gridlab.cli import main

def test_case_listing_is_available_without_running_a_simulation(capsys):
    assert main(["list"]) == 0
    assert "island-recovery:" in capsys.readouterr().out

def test_cli_run_writes_parseable_metrics_and_report(tmp_path, capsys):
    assert main(["run", "--duration", ".1", "--output", str(tmp_path)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["metrics"]["duration_s"] == .1
    assert (tmp_path/"trace.npz").exists()

def test_invalid_duration_is_actionable():
    with pytest.raises(SystemExit) as e:
        main(["run", "--duration", "-1"])
    assert e.value.code == 2
