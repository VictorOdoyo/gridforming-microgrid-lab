import numpy as np

from gridlab.frequency_response import frequency_response


def test_first_order_lowpass_matches_closed_form():
    w = np.array([0, 1, 10])
    response = frequency_response([[-2]], [[2]], [[1]], [[0]], w)
    np.testing.assert_allclose(response[:, 0, 0], 2 / (2 + 1j * w))
