"""Provenance descriptors for the exact default study models and parameters."""

from dataclasses import asdict, dataclass

from gridlab.converter.active_damping import default_lcl
from gridlab.converter.lc import LCPlant
from gridlab.dc.system import DCSystem


@dataclass(frozen=True)
class StudySpec:
    name: str
    model: dict
    parameters: dict


def specification(name):
    if name == "sample-delay":
        return StudySpec(
            name,
            asdict(LCPlant()),
            {
                "conductance": 0.1,
                "periods_s": [0.000025, 0.00005, 0.0001, 0.0002],
                "delay_samples": [0, 1, 2],
                "current_bandwidth_hz": 1000,
                "voltage_bandwidth_hz": 50,
                "dc_voltage_v": 700,
                "reference_peak_v": 325,
            },
        )
    if name == "dc-convergence":
        return StudySpec(
            name,
            asdict(DCSystem()),
            {
                "duration_s": 0.05,
                "control_period_s": 0.0001,
                "integration_substeps": [1, 2, 4],
                "reference_substeps": 8,
                "demand_times_s": [0, 0.02],
                "demand_w": [30000, 60000],
            },
        )
    if name == "observer":
        return StudySpec(
            name,
            asdict(LCPlant()),
            {
                "seed": 42,
                "noise_std_v": 1,
                "steps": 1000,
                "control_period_s": 0.00005,
                "conductance": 0.1,
                "command_dq_v": [330, 10],
            },
        )
    if name == "active-damping":
        return StudySpec(name, asdict(default_lcl()), {"gains_ohm": [0, 0.5, 1, 2, 5]})
    raise ValueError("unsupported physical study")


def specification_dict(spec):
    return {"schema_version": 1, **asdict(spec)}
