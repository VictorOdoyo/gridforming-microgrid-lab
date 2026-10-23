import pytest

from gridlab.lab.cases import converter_step
from gridlab.lab.timing import retime


def test_shortening_a_reference_ramp_preserves_original_slope():
    c = converter_step()
    short = retime(c, 0.01)
    assert short.signals["reference_v"](0.005) == pytest.approx(c.signals["reference_v"](0.005))
    assert short.duration == 0.01
    with pytest.raises(ValueError):
        retime(c, -1)
