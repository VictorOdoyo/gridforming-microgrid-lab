"""Measurement chain for LC dq states; RNG state advances only at control ticks."""

from collections import deque
from dataclasses import dataclass, field

import numpy as np

from .adc import ADC


class SampleDelay:
    def __init__(self, samples, initial):
        if not isinstance(samples, int) or samples < 0:
            raise ValueError("nonnegative integer sample delay required")
        self.buffer = deque([np.array(initial, copy=True) for _ in range(samples)])
        self.samples = samples

    def step(self, value):
        value = np.array(value, copy=True)
        if not self.samples:
            return value
        self.buffer.append(value)
        return self.buffer.popleft()


@dataclass
class SensorChain:
    bits: int = 12
    current_full_scale_a: float = 200
    voltage_full_scale_v: float = 500
    noise_std: float = 0
    delay_samples: int = 0
    seed: int = 42
    gain: float = 1
    offset: float = 0
    rng: object = field(init=False)
    delay: object = field(init=False)

    def __post_init__(self):
        if self.noise_std < 0:
            raise ValueError("nonnegative sensor noise required")
        self.rng = np.random.default_rng(self.seed)
        self.delay = SampleDelay(self.delay_samples, np.zeros(4))

    def __call__(self, state):
        x = np.asarray(state) * self.gain + self.offset + self.rng.normal(0, self.noise_std, 4)
        measured = np.r_[
            ADC(self.bits, self.current_full_scale_a).measure(x[:2]),
            ADC(self.bits, self.voltage_full_scale_v).measure(x[2:]),
        ]
        return self.delay.step(measured)
