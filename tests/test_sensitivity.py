import pytest
from gridlab.sensitivity import sensitivity

def test_square_law_elasticity():
    s = sensitivity(lambda x: 3*x*x, 2)
    assert s.derivative == pytest.approx(12)
    assert s.elasticity == pytest.approx(2)
