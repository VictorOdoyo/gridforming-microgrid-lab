from gridlab.dc.system import DCSystem
from gridlab.lab.case import LabCase, run_case
from gridlab.lab.plotting import plot_case


def test_physical_figure_is_exportable(tmp_path):
    c = LabCase("dc", "dc", "DC figure", DCSystem(), 0.002)
    assert plot_case(c, run_case(c), tmp_path / "response.svg").stat().st_size > 1000
