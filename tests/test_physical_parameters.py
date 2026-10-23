import pytest

from gridlab.converter.lc import LCPlant
from gridlab.dc.bidirectional import Bidirectional
from gridlab.dc.bus import Bus
from gridlab.dc.electrochem import Polarization
from gridlab.dc.pack import Pack
from gridlab.dc.system import DCSystem
from gridlab.hybrid.grid_forming import GridForming


@pytest.mark.parametrize(
    "factory,key",
    [
        (Pack, "capacity_ah"),
        (Bus, "capacitance_f"),
        (Bidirectional, "inductance_h"),
        (Polarization, "capacitance_f"),
        (DCSystem, "ambient_c"),
        (LCPlant, "omega"),
        (GridForming, "inertia_s"),
    ],
)
@pytest.mark.parametrize("value", [float("nan"), float("inf")])
def test_nonfinite_physical_parameters_fail_at_construction(factory, key, value):
    with pytest.raises(ValueError):
        factory(**{key: value})
