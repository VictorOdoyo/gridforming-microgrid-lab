"""Average converter simulation; no switching harmonics are implied."""

from dataclasses import dataclass

import numpy as np

from gridlab.numerics import merge_boundaries, rk4, ticks

from .control import Cascade
from .lc import LCPlant


@dataclass(frozen=True)
class ConverterTrace:
    time: np.ndarray
    state: np.ndarray
    command: np.ndarray
    reference: np.ndarray
    conductance: np.ndarray
    dc_voltage: np.ndarray


def simulate_converter(
    plant=None,
    duration=0.25,
    period_s=0.00005,
    reference=None,
    conductance=None,
    dc_voltage=None,
    initial=None,
    control=None,
    measurement=None,
    actuation_delay=None,
    boundaries=(),
):
    plant = plant or LCPlant()
    control = control or Cascade.tuned(plant)
    reference = reference or (lambda t: 325 * min(1, t / 0.02))
    conductance = conductance or (lambda t: 0.1 if t < 0.08 else 0.2)
    dc_voltage = dc_voltage or (lambda t: 700.0)
    time = merge_boundaries(ticks(duration, period_s), boundaries)
    x = np.zeros(4) if initial is None else np.array(initial, float)
    states, commands, refs, loads, links = [], [], [], [], []
    for k, t in enumerate(time):
        dt = time[k + 1] - t if k + 1 < len(time) else period_s
        ref, g, link = complex(reference(t)), float(conductance(t)), float(dc_voltage(t))
        measured = x if measurement is None else np.asarray(measurement(x))
        command = control.step(plant, measured, ref, link, g, dt)
        if actuation_delay is not None:
            delayed = actuation_delay.step([command.real, command.imag])
            command = complex(*delayed)
        states.append(x.copy())
        commands.append(command)
        refs.append(ref)
        loads.append(g)
        links.append(link)
        if k + 1 < len(time):
            x = rk4(lambda now, state: plant.derivative(state, command, g), t, x, dt)
    return ConverterTrace(
        time, np.array(states), np.array(commands), np.array(refs), np.array(loads), np.array(links)
    )
