"""Branch power accounting, including shunt charging."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BranchFlow:
    sending: complex
    receiving: complex
    loss: complex
    series_current: complex


def branch_flow(line, voltage):
    if not line.enabled:
        return BranchFlow(0j, 0j, 0j, 0j)
    vi, vj = voltage[line.start], voltage[line.end]
    current = (vi - vj) / line.impedance
    si = vi * np.conj(current + 0.5j * line.b * vi)
    sj = vj * np.conj(-current + 0.5j * line.b * vj)
    return BranchFlow(si, sj, si + sj, current)


def balance_error(source_power, load_power, lines, voltage):
    loss = sum((branch_flow(line, voltage).loss for line in lines), 0j)
    return sum(source_power) - sum(load_power) - loss
