"""Observer experiment on the exact discrete LC plant with seeded voltage noise."""

import numpy as np

from gridlab.converter.lc import LCPlant
from gridlab.converter.observer import KalmanObserver
from gridlab.converter.state_space import lc_state_space
from gridlab.discrete import zero_order_hold


def observer_study(seed=42, noise_std_v=1, steps=1000):
    if noise_std_v <= 0 or steps < 20:
        raise ValueError("positive noise and at least twenty steps required")
    a, b = lc_state_space(LCPlant(), 0.1)
    ad, bd = zero_order_hold(a, b, 0.00005)
    h = np.eye(4)[2:]
    observer = KalmanObserver(
        ad, bd, h, np.eye(4) * 1e-5, np.eye(2) * noise_std_v**2, np.zeros(4), np.eye(4) * 100
    )
    rng = np.random.default_rng(seed)
    state = np.array([20.0, -5, 300, 10])
    errors = []
    for _ in range(steps):
        state = ad @ state + bd @ [330, 10]
        estimate = observer.step(np.array([330, 10]), h @ state + rng.normal(0, noise_std_v, 2))
        errors.append(estimate - state)
    e = np.array(errors)[steps // 2 :]
    rms = np.sqrt(np.mean(e**2, axis=0))
    return {
        "seed": seed,
        "noise_std_v": noise_std_v,
        "steps": steps,
        "current_d_rms_error_a": float(rms[0]),
        "current_q_rms_error_a": float(rms[1]),
        "voltage_d_rms_error_v": float(rms[2]),
        "voltage_q_rms_error_v": float(rms[3]),
        "minimum_covariance_eigenvalue": float(np.linalg.eigvalsh(observer.covariance).min()),
    }
