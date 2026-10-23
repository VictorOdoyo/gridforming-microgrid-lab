"""Biorthogonal eigenvector participation, normalized per mode for ranking."""

import numpy as np


def participation(matrix):
    eigenvalues, right = np.linalg.eig(np.asarray(matrix, float))
    if np.linalg.cond(right) > 1e12:
        raise ValueError("eigenvectors are ill-conditioned; participation is unreliable")
    left = np.linalg.inv(right)
    factors = abs(right * left.T)
    factors /= np.maximum(factors.sum(axis=0, keepdims=True), 1e-30)
    return eigenvalues, factors
