import numpy as np

from gridlab.lab.case import run_case
from gridlab.lab.cases import converter_sag


def test_named_sag_case_obeys_current_dc_modulation_ceiling():
    r = run_case(converter_sag())
    assert np.max(abs(r.command) - r.dc_voltage / np.sqrt(3)) < 1e-9
    assert abs(complex(*r.state[-1, 2:]) - 325) < 1
