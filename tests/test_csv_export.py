import csv
from gridlab.config import Inverter, Microgrid
from gridlab.simulation import simulate
from gridlab.csv_export import export_csv

def test_csv_has_explicit_units_and_trace_endpoints(tmp_path):
    r = simulate(Microgrid(1, (), (.3+.1j,), (Inverter("battery, A", 0),)), .1)
    path = export_csv(r, tmp_path/"trace.csv")
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[-1]["entity"] == "battery, A"
    assert float(rows[-1]["time_s"]) == .1
    assert {x["unit"] for x in rows} == {"pu", "rad", "bool", "Hz"}
