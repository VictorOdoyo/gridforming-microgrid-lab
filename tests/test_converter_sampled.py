from gridlab.converter.lc import LCPlant
from gridlab.converter.sampled import sampled_cascade


def test_discrete_analysis_detects_excessive_control_period():
    normal = sampled_cascade(LCPlant())
    slow = sampled_cascade(LCPlant(), period_s=0.0005)
    assert normal["fixed_point_residual"] < 1e-8
    assert normal["spectral_radius"] < 1
    assert slow["spectral_radius"] > 1
