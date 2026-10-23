from gridlab.config import Inverter, Microgrid
from gridlab.simulation import simulate
from gridlab.plotting import plot_result

def test_figure_exports_both_raster_and_vector(tmp_path):
    r = simulate(Microgrid(1, (), (.3+.1j,), (Inverter("a", 0),)), .1)
    for extension in ("png", "svg"):
        p = plot_result(r, tmp_path/f"response.{extension}")
        assert p.stat().st_size > 1000
