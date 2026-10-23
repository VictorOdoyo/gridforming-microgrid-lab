"""SI dq filter: L di/dt = v_converter - v_bus - R i - j omega L i."""
from dataclasses import dataclass

@dataclass(frozen=True)
class RLFilter:
    resistance_ohm: float
    inductance_h: float

    def __post_init__(self):
        if self.resistance_ohm < 0 or self.inductance_h <= 0:
            raise ValueError("invalid RL parameters")

    def derivative(self, current_dq, converter_dq, bus_dq, omega):
        return ((converter_dq-bus_dq-self.resistance_ohm*current_dq)/self.inductance_h
                - 1j*omega*current_dq)

    def energy_j(self, current_dq):
        # amplitude-invariant dq peak convention: three-phase magnetic energy
        return .75*self.inductance_h*abs(current_dq)**2
