"""Wide CSV with units encoded in column names and original controller records."""

import csv
from pathlib import Path

_DC = ("soc", "polarization_v", "battery_inductor_a", "dc_energy_j", "pack_temperature_c")
_AC = ("inductor_d_peak_a", "inductor_q_peak_a", "bus_d_peak_v", "bus_q_peak_v")
_OUTER = ("oscillator_angle_rad", "oscillator_deviation_hz", "filtered_power_pu", "secondary_bias_hz")


def columns(case, trace):
    names = _DC if case.kind == "dc" else _AC if case.kind == "converter" else _DC + _AC
    if case.kind == "hybrid" and trace.state.shape[1] == 13:
        names += _OUTER
    output = {"time_s": trace.time, **{name: trace.state[:, k] for k, name in enumerate(names)}}
    for name in (
        "precharge",
        "duty",
        "closed",
        "gate",
        "demand_w",
        "conductance",
        "dc_voltage",
        "solar_w",
        "reference_a",
    ):
        if hasattr(trace, name):
            output[name] = getattr(trace, name)
    for name in ("command", "reference"):
        if hasattr(trace, name):
            output[name + "_d_peak_v"] = getattr(trace, name).real
            output[name + "_q_peak_v"] = getattr(trace, name).imag
    return output


def export_csv(case, trace, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = columns(case, trace)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(data)
        writer.writerows(zip(*data.values(), strict=True))
    return path
