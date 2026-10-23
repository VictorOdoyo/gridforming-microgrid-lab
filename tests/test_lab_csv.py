import csv

from gridlab.hybrid.plant import HybridPlant
from gridlab.lab.case import LabCase, run_case
from gridlab.lab.csv_export import export_csv


def test_hybrid_csv_retains_dc_and_ac_state_units(tmp_path):
    c = LabCase("short", "hybrid", "csv", HybridPlant(), 0.002)
    r = run_case(c)
    path = export_csv(c, r, tmp_path / "trace.csv")
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == len(r.time)
    assert "battery_inductor_a" in rows[0] and "bus_d_peak_v" in rows[0]
    assert float(rows[-1]["time_s"]) == 0.002
