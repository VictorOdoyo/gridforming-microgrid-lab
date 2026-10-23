"""Spectral-radius study for local unsaturated sampled converter control."""

from .lc import LCPlant
from .sampled import sampled_cascade


def delay_study(periods=(0.000025, 0.00005, 0.0001, 0.0002), delays=(0, 1, 2)):
    rows = []
    for period in periods:
        for delay in delays:
            report = sampled_cascade(LCPlant(), period_s=period, delay_samples=delay)
            radius = report["spectral_radius"]
            rows.append(
                {
                    "period_s": period,
                    "delay_samples": delay,
                    "delay_s": period * delay,
                    "spectral_radius": radius,
                    "stable": radius < 1,
                }
            )
    return rows
