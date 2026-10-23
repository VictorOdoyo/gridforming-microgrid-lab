"""Reduced phasor dynamics; state per source is angle, df, E, filtered P, filtered Q."""
import numpy as np
from .network import admittance
from .norton import solve_network
from .secondary import secondary_rate

class Dynamics:
    def __init__(self, config, load_scale=1.0, enabled=None):
        self.config = config
        self.n = len(config.inverters)
        self.enabled = np.ones(self.n, bool) if enabled is None else np.array(enabled, bool)
        self.ybus = admittance(config.nbus, config.lines, np.conj(config.loads)*load_scale)
        self.buses = [i.bus for i in config.inverters]
        self.impedances = [i.impedance for i in config.inverters]

    def initial(self, voltage=1.0):
        state = np.zeros(5*self.n+1)
        state[:-1].reshape(self.n, 5)[:, 2] = voltage
        point = self.network(state)
        state[:-1].reshape(self.n, 5)[:, 3] = point.power.real
        state[:-1].reshape(self.n, 5)[:, 4] = point.power.imag
        return state

    def network(self, state):
        x = state[:-1].reshape(self.n, 5)
        emf = x[:, 2]*np.exp(1j*x[:, 0])
        return solve_network(self.ybus, self.buses, self.impedances, emf, self.enabled)

    def frequencies(self, state):
        x = state[:-1].reshape(self.n, 5)
        return np.array([x[k, 1] if inv.mode == "vsm"
                         else inv.droop_hz*(inv.p_ref-x[k, 3])+state[-1]
                         for k, inv in enumerate(self.config.inverters)])

    def __call__(self, time, state):
        x = state[:-1].reshape(self.n, 5)
        dx = np.zeros_like(x)
        point = self.network(state)
        df = self.frequencies(state)
        for k, inv in enumerate(self.config.inverters):
            if not self.enabled[k]:
                continue
            dx[k, 0] = 2*np.pi*df[k]
            if inv.mode == "vsm":
                dx[k, 1] = self.config.base.frequency_hz/(2*inv.inertia_s)*(
                    inv.p_ref-x[k, 3]-(df[k]-state[-1])/inv.droop_hz)
            target = inv.v_ref-inv.q_droop*(x[k, 4]-inv.q_ref)
            dx[k, 2] = (target-x[k, 2])/inv.voltage_tau
            dx[k, 3] = (point.power[k].real-x[k, 3])/inv.power_tau
            dx[k, 4] = (point.power[k].imag-x[k, 4])/inv.power_tau
        active = df[self.enabled]
        ds = secondary_rate(active, state[-1], self.config.secondary_gain,
                            self.config.secondary_limit_hz) if len(active) else 0.0
        return np.r_[dx.ravel(), ds]
