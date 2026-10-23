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


def converter_sag():
    from dataclasses import replace

    base = converter_step()
    return replace(
        base,
        name="converter-sag",
        description="DC sag saturates modulation before AC voltage recovers",
        duration=0.35,
        signals={
            **base.signals,
            "conductance": Signal((0,), (0.1,)),
            "dc_voltage_v": Signal((0, 0.08, 0.15), (700, 450, 700)),
        },
    )


CASES["converter-sag"] = converter_sag


def hybrid_step(mode="vsm"):
    from gridlab.hybrid.grid_forming import GridForming
    from gridlab.hybrid.plant import HybridPlant

    return LabCase(
        "hybrid-step",
        "hybrid",
        "Battery-fed grid-forming inverter responds to an AC load step",
        HybridPlant(outer=GridForming(mode=mode)),
        0.3,
        0.0001,
        {"reference_v": Signal((0, 0.02), (0, 325), "linear"), "conductance": Signal((0, 0.1), (0.1, 0.2))},
    )


CASES["hybrid-step"] = hybrid_step


def hybrid_outage():
    from dataclasses import replace

    from gridlab.hybrid.events import HybridEvent

    base = hybrid_step()
    return replace(
        base,
        name="hybrid-outage",
        description="Battery trip drains DC hold-up before protected AC isolation",
        duration=0.5,
        events=(HybridEvent(0.1, "battery-trip"),),
    )


CASES["hybrid-outage"] = hybrid_outage


def hybrid_restart():
    from dataclasses import replace

    from gridlab.hybrid.events import HybridEvent

    base = hybrid_outage()
    return replace(
        base,
        name="hybrid-restart",
        description="Battery rearm recharges DC link before guarded AC restart",
        duration=0.9,
        events=(*base.events, HybridEvent(0.4, "battery-reset"), HybridEvent(0.4, "gate-reset")),
    )


CASES["hybrid-restart"] = hybrid_restart


def hybrid_cloud():
    from dataclasses import replace

    base = hybrid_step()
    return replace(
        base,
        name="hybrid-cloud",
        description="Solar surplus charges storage before a cloud removes DC injection",
        duration=0.4,
        signals={
            **base.signals,
            "conductance": Signal((0,), (0.1,)),
            "solar_w": Signal((0, 0.06, 0.2), (0, 30000, 0)),
        },
    )


CASES["hybrid-cloud"] = hybrid_cloud
