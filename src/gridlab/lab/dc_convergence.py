"""Convergence of physical integration, distinct from changing digital controller bandwidth."""

from gridlab.dc.audit import audit_dc
from gridlab.dc.simulation import simulate_dc
from gridlab.dc.system import DCSystem


def dc_convergence(substeps=(1, 2, 4), duration=0.05):
    plant = DCSystem()

    def demand(t):
        return 30000 if t < 0.02 else 60000

    reference = simulate_dc(plant, demand, duration, integration_substeps=8)
    rows = []
    for count in substeps:
        result = simulate_dc(plant, demand, duration, integration_substeps=count)
        error = abs(result.state - reference.state)
        rows.append(
            {
                "integration_substeps": count,
                "control_period_s": 0.0001,
                "maximum_soc_error": float(error[:, 0].max()),
                "maximum_inductor_error_a": float(error[:, 2].max()),
                "maximum_capacitor_energy_error_j": float(error[:, 3].max()),
                "relative_energy_residual": audit_dc(plant, result)["relative_residual"],
            }
        )
    return rows
