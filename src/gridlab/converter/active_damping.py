"""Virtual damping voltage proportional to measured capacitor current."""

import numpy as np

from gridlab.lcl import LCLFilter


def damping_command(reference, current_converter, current_grid, gain_ohm):
    if gain_ohm < 0:
        raise ValueError("nonnegative damping gain required")
    return reference - gain_ohm * (current_converter - current_grid)


def lcl_matrix(plant, gain_ohm=0):
    if gain_ohm < 0:
        raise ValueError("nonnegative active damping required")
    a = np.array(
        [
            [-(plant.r1 + gain_ohm) / plant.l1, -1 / plant.l1, gain_ohm / plant.l1],
            [1 / plant.capacitance, 0, -1 / plant.capacitance],
            [0, 1 / plant.l2, -plant.r2 / plant.l2],
        ]
    )
    return a


def default_lcl():
    return LCLFilter(0.001, 0.002, 20e-6, 0.05, 0.05)
