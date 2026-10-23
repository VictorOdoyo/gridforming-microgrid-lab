"""Independent storage audit using exact OCV integration and held-load intervals."""

import numpy as np

from .chemical import chemical_energy


def stored(system, state):
    return state[3] + system.converter.stored_j(state[2]) + system.polarization.stored_j(state[1])


def audit_dc(system, trace):
    if len(trace.time) < 2:
        raise ValueError("at least two samples required for energy audit")
    heat = 0.0
    cooling = 0.0
    for k, dt in enumerate(np.diff(trace.time)):
        observations = [
            system.observe(trace.state[j], trace.duty[k], bool(trace.closed[k])) for j in (k, k + 1)
        ]
        heat += dt * sum(p["heat_w"] for p in observations) / 2
        cooling += (
            dt
            * sum((trace.state[j, 4] - system.ambient_c) / system.thermal_resistance_k_w for j in (k, k + 1))
            / 2
        )
    chemical = chemical_energy(system.pack, trace.state[0, 0]) - chemical_energy(
        system.pack, trace.state[-1, 0]
    )
    output = float(np.dot(np.diff(trace.time), trace.demand_w[:-1]))
    delta = stored(system, trace.state[-1]) - stored(system, trace.state[0])
    residual = chemical - output - heat - delta
    return {
        "chemical_draw_j": chemical,
        "delivered_j": output,
        "heat_j": heat,
        "stored_delta_j": delta,
        "residual_j": residual,
        "relative_residual": abs(residual) / max(abs(chemical), abs(output), 1),
        "thermal_residual_j": heat
        - cooling
        - system.thermal_capacity_j_k * (trace.state[-1, 4] - trace.state[0, 4]),
    }
