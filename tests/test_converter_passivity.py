import numpy as np

from gridlab.converter.lc import LCPlant
from gridlab.converter.passivity import dissipation_matrix, passive


def test_energy_certificate_matches_copper_and_load_dissipation():
    plant = LCPlant()
    d = dissipation_matrix(plant, 0.2)
    np.testing.assert_allclose(d, 1.5 * np.diag([0.1, 0.1, 0.2, 0.2]), atol=1e-12)
    assert passive(plant, 0.2)
    assert passive(LCPlant(resistance_ohm=0), 0)
