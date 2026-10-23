"""Grid-strength experiment with one connected source and an active-power step."""

from .config import GridConnection, Inverter, Microgrid
from .events import Event, run_events
from .grid_strength import short_circuit_ratio
from .metrics import frequency_metrics
from .quality import voltage_metrics


def weak_grid_study(reactances=(0.05, 0.2, 0.5), mode="vsm", duration=5.0):
    if duration <= 1:
        raise ValueError("study must include the disturbance at 1 s")
    rows = []
    for x in reactances:
        grid = GridConnection(impedance=0.02 + 1j * x)
        config = Microgrid(1, (), (0.4 + 0.1j,), (Inverter("bess", 0, p_ref=0.2, mode=mode),), grid=grid)
        trace = run_events(config, (Event(1, "p_ref", 0.5),), duration, sample_s=0.05, max_step=0.05)
        rows.append(
            {
                "reactance_pu": x,
                "scr": short_circuit_ratio(grid.impedance, 1),
                **frequency_metrics(trace.time, trace.frequency_hz),
                **voltage_metrics(trace.time, trace.voltage),
            }
        )
    return rows
