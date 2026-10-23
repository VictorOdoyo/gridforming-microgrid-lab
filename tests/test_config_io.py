import pytest

from gridlab.cases import island_recovery, overload
from gridlab.config_io import load_case, parse_case, save_case


@pytest.mark.parametrize("factory", [island_recovery, overload])
def test_case_roundtrip_preserves_controller_and_network(tmp_path, factory):
    case = factory()
    path = tmp_path / "case.json"
    save_case(case, path)
    assert load_case(path) == case


def test_unknown_schema_rejected():
    with pytest.raises(ValueError):
        parse_case({"schema_version": 2})
