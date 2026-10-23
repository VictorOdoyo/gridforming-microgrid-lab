from dataclasses import replace
import numpy as np
from gridlab.cases import load_step
from gridlab.dynamics import Dynamics
from gridlab.operating_point import operating_point
from gridlab.simulation import simulate
from gridlab.stability import stability_report

def test_default_vsm_is_stable_under_asymmetric_angle_perturbation():
    c = load_step("vsm").config
    op = operating_point(c)
    x = op.state.copy()
    x[5] += .001
    r = simulate(c, 5, initial=x)
    differential = r.frequency_hz[:, 0]-r.frequency_hz[:, 1]
    assert max(abs(differential[-25:])) < .002
    assert stability_report(c)["spectral_abscissa"] < 0

def test_slow_power_filter_exposes_unstable_relative_mode():
    c = load_step("vsm").config
    c = replace(c, inverters=tuple(replace(i, power_tau=.05) for i in c.inverters))
    assert stability_report(c)["spectral_abscissa"] > 0
