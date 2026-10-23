import json

import pytest

from gridlab.cli import main


def test_physical_mode_override_is_saved_with_the_reproducible_case(tmp_path, capsys):
    assert main(["lab", "run", "--mode", "droop", "--duration", ".002", "--output", str(tmp_path)]) == 0
    case = json.loads((tmp_path / "case.json").read_text())
    assert case["plant"]["outer"]["mode"] == "droop"
    with pytest.raises(SystemExit):
        main(["lab", "run", "--case", "dc-step", "--mode", "vsm", "--duration", ".002"])
