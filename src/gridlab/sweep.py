"""Deterministic study execution with explicit per-case failures."""

from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Trial:
    parameters: dict
    result: object = None
    error: str | None = None


def parameter_grid(axes):
    keys = tuple(axes)
    if any(not len(axes[k]) for k in keys):
        raise ValueError("parameter axes must be nonempty")
    return [dict(zip(keys, values)) for values in product(*(axes[k] for k in keys))]


def run_sweep(function, parameters, fail_fast=False):
    trials = []
    for case in parameters:
        try:
            trials.append(Trial(dict(case), function(**case)))
        except (ValueError, RuntimeError, ArithmeticError) as exc:
            if fail_fast:
                raise
            trials.append(Trial(dict(case), error=f"{type(exc).__name__}: {exc}"))
    return trials
