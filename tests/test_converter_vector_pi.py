import pytest

from gridlab.converter.vector_pi import VectorPI


def test_vector_limit_and_bumpless_output_tracking():
    c = VectorPI(2, 10)
    c.track(3 + 4j, 1j, 2)
    assert c.step(1j, 2, 10, 0.001) == pytest.approx(3 + 4j)
    for _ in range(1000):
        assert abs(c.step(100 + 100j, 0, 5, 0.001)) <= 5 + 1e-12
    assert abs(c.integral) < 300
