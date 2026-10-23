"""Timing overrides preserve signal values before the new endpoint."""

from dataclasses import replace

from .signals import Signal


def retime(case, duration=None, period_s=None):
    horizon = case.duration if duration is None else duration
    if horizon <= 0:
        raise ValueError("positive duration required")
    signals = {}
    for name, s in case.signals.items():
        times = [t for t in s.times if t <= horizon]
        if not times:
            times = [0.0]
        if horizon < s.times[-1] and times[-1] != horizon:
            times.append(horizon)
        signals[name] = Signal(tuple(times), tuple(float(s(t)) for t in times), s.interpolation)
    return replace(
        case,
        duration=horizon,
        period_s=case.period_s if period_s is None else period_s,
        signals=signals,
        events=tuple(e for e in case.events if e.time <= horizon),
    )
