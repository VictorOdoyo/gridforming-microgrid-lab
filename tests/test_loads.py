import numpy as np
from gridlab.loads import ZIPLoad

def test_zip_voltage_laws():
    v = .8
    assert ZIPLoad(1).demand(v) == v*v
    assert ZIPLoad(1, 0, 1, 0).demand(v) == v
    assert ZIPLoad(1, 0, 0, 1).demand(v) == 1
    np.testing.assert_allclose(ZIPLoad(1+.3j).current(1), 1-.3j)

def test_black_bus_has_finite_foldback_current():
    assert ZIPLoad(1, 0, 0, 1).current(0) == 0
