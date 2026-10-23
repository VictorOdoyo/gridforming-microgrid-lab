import numpy as np

from gridlab.converter.lc import LCPlant
from gridlab.converter.observer import KalmanObserver
from gridlab.converter.state_space import lc_state_space
from gridlab.discrete import zero_order_hold


def test_voltage_only_observer_recovers_current_and_preserves_psd_covariance():
    a, b = lc_state_space(LCPlant(), 0.1)
    ad, bd = zero_order_hold(a, b, 0.0001)
    h = np.eye(4)[2:]
    observer = KalmanObserver(ad, bd, h, np.eye(4) * 1e-6, np.eye(2) * 0.01, np.zeros(4), np.eye(4) * 100)
    truth = np.array([10.0, -2, 300, 5])
    for _ in range(300):
        truth = ad @ truth + bd @ [330, 0]
        estimate = observer.step(np.array([330, 0]), h @ truth)
    assert np.linalg.norm(estimate - truth) < 0.01
    assert np.linalg.eigvalsh(observer.covariance).min() >= 0
