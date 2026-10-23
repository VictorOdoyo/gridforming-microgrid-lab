import pytest

from gridlab.rlfilter import RLFilter


def test_steady_state_impedance_and_passive_decay():
    f = RLFilter(0.1, 0.002)
    i = 10 - 3j
    v = (0.1 + 1j * 314 * 0.002) * i
    assert abs(f.derivative(i, v, 0, 314)) < 1e-10
    di = f.derivative(i, 0, 0, 314)
    assert (i.conjugate() * di).real == pytest.approx(-0.1 / 0.002 * abs(i) ** 2)
