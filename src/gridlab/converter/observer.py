"""Linear observer with Joseph covariance update and explicit measurement covariance."""

from dataclasses import dataclass

import numpy as np


@dataclass
class KalmanObserver:
    transition: np.ndarray
    input_matrix: np.ndarray
    measurement_matrix: np.ndarray
    process_covariance: np.ndarray
    measurement_covariance: np.ndarray
    state: np.ndarray
    covariance: np.ndarray

    def step(self, command, measurement):
        a, b, h = self.transition, self.input_matrix, self.measurement_matrix
        predicted = a @ self.state + b @ command
        prior = a @ self.covariance @ a.T + self.process_covariance
        innovation_covariance = h @ prior @ h.T + self.measurement_covariance
        gain = np.linalg.solve(innovation_covariance, (prior @ h.T).T).T
        self.state = predicted + gain @ (measurement - h @ predicted)
        identity = np.eye(len(predicted)) - gain @ h
        self.covariance = identity @ prior @ identity.T + gain @ self.measurement_covariance @ gain.T
        self.covariance = (self.covariance + self.covariance.T) / 2
        return self.state.copy()
