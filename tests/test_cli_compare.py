import json

from gridlab.cli import main


def test_comparison_produces_both_reproducible_experiments(tmp_path, capsys):
    assert main(["compare", "--duration", ".1", "--output", str(tmp_path)]) == 0
    summaries = json.loads(capsys.readouterr().out)
    assert set(summaries) == {"droop", "vsm"}
    assert (tmp_path / "droop" / "case.json").exists()
    assert (tmp_path / "vsm" / "trace.npz").exists()
