import json
from gridlab.cli import main
from gridlab.config_io import load_case
from gridlab.events import run_events
from gridlab.storage import save_result

def test_export_then_inspect_workflow(tmp_path, capsys):
    case_path = tmp_path/"case.json"
    assert main(["export-case", "--case", "overload", "--output", str(case_path)]) == 0
    capsys.readouterr()
    c = load_case(case_path)
    result = run_events(c.config, (), .1)
    trace = tmp_path/"trace.npz"
    save_result(result, trace)
    assert main(["inspect", str(trace)]) == 0
    assert json.loads(capsys.readouterr().out)["duration_s"] == .1
