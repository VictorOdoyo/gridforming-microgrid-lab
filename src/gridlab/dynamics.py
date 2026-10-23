"""Reduced phasor dynamics; state per source is angle, df, E, filtered P, filtered Q."""
import numpy as np
from .network import admittance
from .norton import NetworkPoint
from .limited_network import solve_limited
from .secondary import secondary_rate
from .synchronization import phase_correction

class Dynamics:
    def __init__(self, config, load_scale=1.0, enabled=None, grid_connected=None):
        self.config = config
        self.n = len(config.inverters)
        self.grid_connected = (config.grid is not None and config.grid.initially_connected
                               if grid_connected is None else grid_connected)
        self.enabled = np.ones(self.n, bool) if enabled is None else np.array(enabled, bool)
        self.ybus = admittance(config.nbus, config.lines, np.conj(config.loads)*load_scale)
        self.buses = [i.bus for i in config.inverters]
        self.impedances = [i.impedance for i in config.inverters]
        self.limits = [i.current_limit_pu for i in config.inverters]

    def initial(self, voltage=None):
        if voltage is None:
            voltage = 0.0 if self.config.startup_s > 0 else 1.0
        state = np.zeros(5*self.n+1)
        state[:-1].reshape(self.n, 5)[:, 2] = voltage
        point = self.network(state)
        state[:-1].reshape(self.n, 5)[:, 3] = point.power.real
        state[:-1].reshape(self.n, 5)[:, 4] = point.power.imag
        return state

    def network(self, state):
        x = state[:-1].reshape(self.n, 5)
        emf = x[:, 2]*np.exp(1j*x[:, 0])
        if self.grid_connected and self.config.grid is not None:
            grid = self.config.grid
            point = solve_limited(self.ybus, [*self.buses, grid.bus],
                                  [*self.impedances, grid.impedance], np.r_[emf, grid.voltage],
                                  [*self.limits, float("inf")], np.r_[self.enabled, True])
            return NetworkPoint(point.voltage, point.current[:self.n], point.power[:self.n], point.residual)
        return solve_limited(self.ybus, self.buses, self.impedances, emf, self.limits, self.enabled)

    def synchronization_bias(self, state):
        if self.config.grid is None or self.grid_connected or self.config.sync_gain == 0:
            return 0.0
        local = self.network(state).voltage[self.config.grid.bus]
        return phase_correction(local, self.config.grid.voltage, self.config.sync_gain)

    def frequencies(self, state):
        x = state[:-1].reshape(self.n, 5)
        return np.array([x[k, 1] if inv.mode == "vsm"
                         else inv.droop_hz*(inv.p_ref-x[k, 3])+state[-1]+self.synchronization_bias(state)
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
                    inv.p_ref-x[k, 3]-(df[k]-state[-1]-self.synchronization_bias(state))/inv.droop_hz)
            startup = min(1.0, max(0.0, time/self.config.startup_s)) if self.config.startup_s else 1.0
            target = startup*(inv.v_ref-inv.q_droop*(x[k, 4]-inv.q_ref))
            dx[k, 2] = (target-x[k, 2])/inv.voltage_tau
            dx[k, 3] = (point.power[k].real-x[k, 3])/inv.power_tau
            dx[k, 4] = (point.power[k].imag-x[k, 4])/inv.power_tau
        active = df[self.enabled]-self.synchronization_bias(state)
        ds = secondary_rate(active, state[-1], self.config.secondary_gain,
                            self.config.secondary_limit_hz) if len(active) else 0.0
        return np.r_[dx.ravel(), ds]
