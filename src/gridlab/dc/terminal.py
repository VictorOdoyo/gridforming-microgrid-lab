"""Select the low-current physical root of P = (Voc - R I) I."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Terminal:
    current_a: float
    voltage_v: float
    power_w: float
    copper_loss_w: float
    limited: bool


def terminal_power(ocv_v, resistance_ohm, requested_w, maximum_current_a=float("inf")):
    if min(ocv_v, resistance_ohm, maximum_current_a) <= 0:
        raise ValueError("positive voltage, resistance, and current limit required")
    if not all(math.isfinite(v) for v in (ocv_v, resistance_ohm, requested_w)):
        raise ValueError("finite electrical inputs required")
    maximum = ocv_v**2 / (4 * resistance_ohm)
    target = min(requested_w, maximum)
    # Stable quadratic evaluation avoids cancellation near zero power.
    current = 2 * target / (ocv_v + math.sqrt(max(0, ocv_v**2 - 4 * resistance_ohm * target)))
    current = max(-maximum_current_a, min(maximum_current_a, current))
    voltage = ocv_v - resistance_ohm * current
    actual = voltage * current
    return Terminal(
        current,
        voltage,
        actual,
        resistance_ohm * current**2,
        not math.isclose(actual, requested_w, rel_tol=1e-10, abs_tol=1e-8),
    )
