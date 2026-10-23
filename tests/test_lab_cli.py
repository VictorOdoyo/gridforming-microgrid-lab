import json

from gridlab.cli import main


def test_physical_cli_lists_runs_and_inspects_original_trace(tmp_path, capsys):
    assert main(["lab", "list"]) == 0
    assert "hybrid-restart [hybrid]" in capsys.readouterr().out
    assert main(["lab", "run", "--case", "dc-step", "--duration", ".002", "--output", str(tmp_path)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["metrics"]["kind"] == "dc"
    assert main(["lab", "inspect", str(tmp_path / "trace.npz")]) == 0
    assert json.loads(capsys.readouterr().out)["duration_s"] == 0.002
