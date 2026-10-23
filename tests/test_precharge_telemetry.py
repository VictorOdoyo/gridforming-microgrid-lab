import csv

import pytest

from gridlab.dc.system import DCSystem
from gridlab.lab.case import LabCase, run_case
from gridlab.lab.csv_export import export_csv
from gridlab.lab.telemetry import dc_currents


def test_terminal_current_records_passive_precharge_while_main_inductor_is_offline(tmp_path):
    plant = DCSystem()
    case = LabCase(
        "precharge",
        "dc",
        "branch currents",
        plant,
        0.002,
        0.0001,
        initial_state=tuple(plant.initial(voltage=500)),
    )
    trace = run_case(case)
    current = dc_currents(case, trace)
    assert trace.state[0, 2] == 0
    assert current["battery_terminal_a"][0] == pytest.approx((620 - 500) / (2 + 0.08))
    export_csv(case, trace, tmp_path / "trace.csv")
    with (tmp_path / "trace.csv").open() as f:
        row = next(csv.DictReader(f))
    assert float(row["precharge_path_a"]) > 50
