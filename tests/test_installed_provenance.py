import gridlab.provenance as module
from gridlab.cases import load_step


def test_installed_package_does_not_discover_a_parent_repository(tmp_path, monkeypatch):
    monkeypatch.setattr(module, "__file__", str(tmp_path / "site-packages" / "gridlab" / "provenance.py"))

    def forbidden(*args, **kwargs):
        raise AssertionError("installed wheel must not discover an unrelated Git ancestor")

    monkeypatch.setattr(module.subprocess, "check_output", forbidden)
    record = module.provenance(load_step())
    assert record["git_commit"] is None
    assert record["git_dirty"] is None
    assert record["package_version"] == "0.2.0"
