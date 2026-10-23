import pytest

from gridlab.converter.lc import LCPlant
from gridlab.lab.case import LabCase
from gridlab.lab.signals import Signal


@pytest.mark.parametrize(
    "signals",
    [
        {"conductnce": Signal((0,), (1,))},
        {"dc_voltage_v": Signal((0,), (0,))},
        {"conductance": Signal((0,), (-1,))},
    ],
)
def test_mistyped_or_nonphysical_case_signals_are_rejected(signals):
    with pytest.raises(ValueError):
        LabCase("bad", "converter", "invalid signal", LCPlant(), 0.1, signals=signals)
