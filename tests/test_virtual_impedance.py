import pytest
from gridlab.virtual_impedance import VirtualImpedance

def test_virtual_drop_and_overcurrent_response():
    z = VirtualImpedance(.02, .1)
    assert z.compensate(1, 1) == pytest.approx(.98-.1j)
    assert z.adaptive(2, 1, .5).resistance == pytest.approx(.52)
    assert z.adaptive(.5, 1, .5) == z
