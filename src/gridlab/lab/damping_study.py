"""LCL pole movement under capacitor-current feedback."""

import numpy as np

from gridlab.converter.active_damping import default_lcl, lcl_matrix


def damping_study(gains=(0, 0.5, 1, 2, 5)):
    rows = []
    for gain in gains:
        poles = np.linalg.eigvals(lcl_matrix(default_lcl(), gain))
        oscillatory = [p for p in poles if abs(p.imag) > 1]
        rows.append(
            {
                "gain_ohm": gain,
                "poles": [[float(p.real), float(p.imag)] for p in poles],
                "maximum_real_pole": float(poles.real.max()),
                "minimum_oscillatory_damping": min((-p.real / abs(p) for p in oscillatory), default=None),
            }
        )
    return rows
