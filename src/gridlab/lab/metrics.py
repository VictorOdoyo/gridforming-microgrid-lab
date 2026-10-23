"""SI trace summaries distinguish physical power from phasor-system pu quantities."""

import numpy as np

from gridlab.dc.audit import audit_dc
from gridlab.hybrid.audit import audit_hybrid


def summarize(case, trace):
    result = {
        "kind": case.kind,
        "duration_s": float(trace.time[-1] - trace.time[0]),
        "samples": len(trace.time),
        "requested_period_s": case.period_s,
    }
    if case.kind in ("dc", "hybrid"):
        system = case.plant if case.kind == "dc" else case.plant.dc
        voltage = np.sqrt(2 * trace.state[:, 3] / system.bus.capacitance_f)
        result.update(
            minimum_dc_v=float(voltage.min()),
            maximum_dc_v=float(voltage.max()),
            final_dc_v=float(voltage[-1]),
            initial_soc=float(trace.state[0, 0]),
            final_soc=float(trace.state[-1, 0]),
            maximum_dc_inductor_a=float(abs(trace.state[:, 2]).max()),
            maximum_battery_a=float(
                max(
                    abs(
                        system.observe(s, trace.duty[k], bool(trace.closed[k]), bool(trace.precharge[k]))[
                            "battery_current_a"
                        ]
                    )
                    for k, s in enumerate(trace.state)
                )
            ),
            precharge_samples=int(trace.precharge.sum()),
            maximum_pack_temperature_c=float(trace.state[:, 4].max()),
        )
    if case.kind == "dc":
        result.update(termination=trace.termination, energy=audit_dc(case.plant, trace))
    else:
        ac = trace.state if case.kind == "converter" else trace.state[:, 5:9]
        peak = ac[:, 2] + 1j * ac[:, 3]
        result.update(
            final_ac_ll_rms_v=float(abs(peak[-1]) * np.sqrt(1.5)),
            final_tracking_error_peak_v=float(abs(peak[-1] - trace.reference[-1])),
            maximum_phase_rms_a=float(np.hypot(ac[:, 0], ac[:, 1]).max() / np.sqrt(2)),
        )
        if case.kind == "hybrid":
            result.update(
                gate_blocked_samples=int((~trace.gate).sum()), energy=audit_hybrid(case.plant, trace)
            )
            if case.plant.outer is not None:
                hz = case.plant.ac.omega / (2 * np.pi)
                frequency = np.array([hz + case.plant.outer.deviation(s[9:13]) for s in trace.state])
                active = frequency[trace.gate]
                result.update(
                    nadir_internal_hz=float(active.min()) if len(active) else None,
                    final_internal_hz=float(frequency[-1]) if trace.gate[-1] else None,
                )
    return result
