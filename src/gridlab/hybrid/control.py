"""Both sampled loops update once per accepted control interval."""

from dataclasses import dataclass, field

from gridlab.converter.control import Cascade
from gridlab.dc.control import DCControl


@dataclass
class HybridControl:
    ac: Cascade
    dc: DCControl = field(default_factory=DCControl)

    @classmethod
    def tuned(cls, plant):
        return cls(Cascade.tuned(plant.ac))

    def step(self, plant, state, reference, conductance, dt, gate=True, reset=False, pv_w=0.0):
        link = plant.dc.bus.voltage(state[3])
        command = self.ac.step(plant.ac, state[5:9], reference, link, conductance, dt) if gate else 0j
        demand = plant.observe(state, 0, command, self.dc.bms.closed, gate)["inverter_dc_w"]
        duty, closed = self.dc.step(plant.dc, state[:5], demand - pv_w, dt, reset)
        return duty, command, closed
