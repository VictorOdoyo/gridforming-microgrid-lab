from dataclasses import replace

from gridlab.cases import load_step
from gridlab.provenance import configuration_hash, provenance


def test_config_hash_changes_with_physical_parameters():
    c = load_step()
    assert configuration_hash(c) == configuration_hash(load_step())
    changed = replace(c, config=replace(c.config, loads=(1 + 0.2j,)))
    assert configuration_hash(changed) != configuration_hash(c)
    record = provenance(c)
    assert "numpy" in record["dependencies"]
    assert len(record["configuration_sha256"]) == 64
