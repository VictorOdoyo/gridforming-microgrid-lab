"""Local stability map, preserving failed operating-point solves as explicit trials."""
from dataclasses import replace
from .cases import load_step
from .stability import stability_report
from .sweep import run_sweep, parameter_grid

def stability_sweep(inertias=(.5, 2, 5), filter_times=(.01, .02, .05)):
    base = load_step("vsm").config
    def evaluate(inertia_s, power_tau):
        c = replace(base, inverters=tuple(replace(i, inertia_s=inertia_s, power_tau=power_tau)
                                         for i in base.inverters))
        report = stability_report(c)
        maximum = report["spectral_abscissa"]
        return {"spectral_abscissa": maximum,
                "stable": all(m["classification"] == "stable" for m in report["modes"])}
    return run_sweep(evaluate, parameter_grid({"inertia_s": inertias, "power_tau": filter_times}))
