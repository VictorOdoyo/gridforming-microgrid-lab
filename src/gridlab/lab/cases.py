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


def dc_hot_pack():
    return LabCase(
        "dc-hot-pack",
        "dc",
        "Thermal current derating limits support from a hot battery",
        DCSystem(ambient_c=55),
        0.25,
        0.0001,
        {"demand_w": Signal((0,), (60000,))},
    )


CASES["dc-hot-pack"] = dc_hot_pack


def converter_step():
    from gridlab.converter.lc import LCPlant

    return LabCase(
        "converter-step",
        "converter",
        "Sampled LC voltage control under a load-conductance step",
        LCPlant(),
        0.25,
        0.00005,
        {
            "reference_v": Signal((0, 0.02), (0, 325), "linear"),
            "conductance": Signal((0, 0.08), (0.1, 0.2)),
            "dc_voltage_v": Signal((0,), (700,)),
        },
    )


CASES["converter-step"] = converter_step
