"""Local linear certificates; remove gauge and inactive states before calling."""
import numpy as np
from scipy.linalg import solve_continuous_lyapunov

def lyapunov_certificate(matrix):
    a = np.asarray(matrix, float)
    if np.max(np.linalg.eigvals(a).real) >= -1e-10:
        raise ValueError("strictly Hurwitz matrix required")
    p = solve_continuous_lyapunov(a.T, -np.eye(len(a)))
    p = (p+p.T)/2
    if np.min(np.linalg.eigvalsh(p)) <= 0:
        raise RuntimeError("positive definite certificate not found")
    return p
