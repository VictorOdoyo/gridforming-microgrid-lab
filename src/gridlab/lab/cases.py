"""Named physical experiments with complete serializable signals."""

from gridlab.dc.system import DCSystem

from .case import LabCase
from .signals import Signal


def dc_step():
    return LabCase(
        "dc-step",
        "dc",
        "Battery DC/DC voltage recovery after a 30 to 60 kW step",
        DCSystem(),
        0.5,
        0.0001,
        {"demand_w": Signal((0, 0.1), (30000, 60000))},
    )


CASES = {"dc-step": dc_step}
