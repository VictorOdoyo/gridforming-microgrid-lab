from gridlab.hybrid.events import HybridEvent
from gridlab.hybrid.grid_forming import GridForming
from gridlab.hybrid.plant import HybridPlant
from gridlab.lab.case import LabCase
from gridlab.lab.config_io import load_case, save_case
from gridlab.lab.signals import Signal


def test_hybrid_case_roundtrip_preserves_physical_parameters_and_events(tmp_path):
    c = LabCase(
        "trip",
        "hybrid",
        "example",
        HybridPlant(outer=GridForming()),
        0.5,
        signals={"solar_w": Signal((0, 0.2), (10000, 0))},
        events=(HybridEvent(0.1, "battery-trip"),),
    )
    path = tmp_path / "case.json"
    save_case(c, path)
    assert load_case(path) == c
