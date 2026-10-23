import numpy as np

from gridlab.converter.adc import ADC


def test_adc_rounding_error_clipping_and_endpoint_codes():
    a = ADC(12, 400)
    values = np.linspace(-400, 400, 1001)
    assert np.max(abs(a.measure(values) - values)) <= a.lsb / 2 + 1e-10
    assert a.encode(500) == 4095 and a.encode(-500) == 0
    np.testing.assert_allclose(a.decode([0, 4095]), [-400, 400])
