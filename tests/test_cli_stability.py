import json

from gridlab.cli import main


def test_stability_command_emits_operating_point_and_modes(capsys):
    assert main(["stability", "--mode", "vsm"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["operating_point_residual"] < 1e-7
    assert data["spectral_abscissa"] < 0
    assert len(data["modes"]) == len(data["state_indices"])
