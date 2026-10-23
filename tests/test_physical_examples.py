from pathlib import Path

import pytest

from gridlab.lab.case import run_case
from gridlab.lab.config_io import load_case
from gridlab.lab.timing import retime


@pytest.mark.parametrize("filename", ["physical-hybrid.json", "physical-dc.json"])
def test_shipped_custom_physical_cases_parse_and_execute(filename):
    path = Path(__file__).parents[1] / "examples" / filename
    c = retime(load_case(path), 0.002)
    r = run_case(c)
    assert r.time[-1] == 0.002
    assert r.state[0, 0] == 0.5
