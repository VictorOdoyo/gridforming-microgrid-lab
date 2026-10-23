"""Complex dq PI with back-calculation after vector saturation."""

from dataclasses import dataclass

from gridlab.modulation import limit_vector


@dataclass
class VectorPI:
    kp: float
    ki: float
    tracking_gain: float = 100
    integral: complex = 0j

    def __post_init__(self):
        if min(self.kp, self.ki, self.tracking_gain) < 0:
            raise ValueError("nonnegative controller gains required")

    def step(self, error, feedforward, maximum, dt):
        if dt <= 0 or maximum <= 0:
            raise ValueError("positive step and output limit required")
        raw = self.kp * error + self.integral + feedforward
        limited = complex(limit_vector(raw, maximum))
        self.integral += dt * (self.ki * error + self.tracking_gain * (limited - raw))
        return limited

    def track(self, output, error=0j, feedforward=0j):
        self.integral = output - self.kp * error - feedforward
