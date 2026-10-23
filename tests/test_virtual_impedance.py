import pytest

from gridlab.virtual_impedance import VirtualImpedance


def test_virtual_drop_and_overcurrent_response():
    z = VirtualImpedance(0.02, 0.1)
    assert z.compensate(1, 1) == pytest.approx(0.98 - 0.1j)
    assert z.adaptive(2, 1, 0.5).resistance == pytest.approx(0.52)
    assert z.adaptive(0.5, 1, 0.5) == z
