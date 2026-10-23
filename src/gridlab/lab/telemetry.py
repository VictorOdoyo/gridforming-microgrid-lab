"""Derived physical branch currents, distinct from stored inductor states."""

import numpy as np


def dc_currents(case, trace):
    if case.kind not in ("dc", "hybrid"):
        raise ValueError("DC telemetry requires a battery-fed physical model")
    system = case.plant if case.kind == "dc" else case.plant.dc
    points = [
        system.observe(s[:5], trace.duty[k], bool(trace.closed[k]), bool(trace.precharge[k]))
        for k, s in enumerate(trace.state)
    ]
    return {
        "battery_terminal_a": np.array([p["battery_current_a"] for p in points]),
        "precharge_path_a": np.array([p["precharge_current_a"] for p in points]),
    }
