"""Whole-system audit without reusing differential equation storage derivatives."""

import numpy as np

from gridlab.dc.chemical import chemical_energy


def audit_hybrid(plant, trace):
    load = 0.0
    heat = 0.0
    for k, dt in enumerate(np.diff(trace.time)):
        loss_values, load_values = [], []
        for state in (trace.state[k], trace.state[k + 1]):
            obs = plant.observe(
                state, trace.duty[k], trace.command[k], bool(trace.closed[k]), bool(trace.gate[k])
            )
            ac = state[5:9]
            copper = 1.5 * plant.ac.resistance_ohm * np.dot(ac[:2], ac[:2])
            loss_values.append(obs["heat_w"] + obs["inverter_loss_w"] + copper)
            load_values.append(1.5 * trace.conductance[k] * np.dot(ac[2:], ac[2:]))
        heat += dt * sum(loss_values) / 2
        load += dt * sum(load_values) / 2
    chemical = chemical_energy(plant.dc.pack, trace.state[0, 0]) - chemical_energy(
        plant.dc.pack, trace.state[-1, 0]
    )
    delta = plant.stored_j(trace.state[-1]) - plant.stored_j(trace.state[0])
    residual = chemical - heat - load - delta
    return {
        "chemical_draw_j": chemical,
        "served_load_j": load,
        "loss_j": heat,
        "stored_delta_j": delta,
        "residual_j": residual,
        "relative_residual": abs(residual) / max(abs(chemical), abs(load), 1),
    }
