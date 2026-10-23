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


def dc_reversal():
    return LabCase(
        "dc-reversal",
        "dc",
        "DC load reverses from discharge to regenerative charging",
        DCSystem(),
        0.4,
        0.0001,
        {"demand_w": Signal((0, 0.1), (30000, -30000))},
    )


CASES["dc-reversal"] = dc_reversal


def dc_contactor():
    from gridlab.dc.events import DCEvent

    return LabCase(
        "dc-contactor",
        "dc",
        "Battery contactor trip and healthy explicit rearm",
        DCSystem(),
        0.2,
        0.0001,
        {"demand_w": Signal((0,), (50000,))},
        (DCEvent(0.05, "trip"), DCEvent(0.06, "reset")),
    )


CASES["dc-contactor"] = dc_contactor
