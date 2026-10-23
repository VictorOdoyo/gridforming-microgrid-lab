"""Three-phase active-power conversion including nonnegative empirical losses."""

import math


def dc_demand(ac_power_w, current_rms_a, resistance_ohm=0.01, fixed_loss_w=20):
    if min(current_rms_a, resistance_ohm, fixed_loss_w) < 0:
        raise ValueError("loss parameters must be nonnegative")
    if not all(math.isfinite(x) for x in (ac_power_w, current_rms_a, resistance_ohm, fixed_loss_w)):
        raise ValueError("finite conversion inputs required")
    loss = fixed_loss_w + 3 * resistance_ohm * current_rms_a**2
    return ac_power_w + loss, loss


def rms_ll_ceiling(dc_voltage_v, modulation_utilization=1.0):
    if dc_voltage_v < 0 or not 0 < modulation_utilization <= 1:
        raise ValueError("invalid DC voltage or modulation utilization")
    return dc_voltage_v * modulation_utilization / math.sqrt(2)
