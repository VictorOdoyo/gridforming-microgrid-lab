"""Balanced Thevenin strength on a common base; assumptions are explicit."""
import numpy as np

def short_circuit_ratio(grid_impedance_pu, inverter_rating_pu, voltage_pu=1.0):
    if abs(grid_impedance_pu) == 0 or min(inverter_rating_pu, voltage_pu) <= 0:
        raise ValueError("nonzero impedance and positive rating required")
    return voltage_pu**2/(abs(grid_impedance_pu)*inverter_rating_pu)

def transfer_power(emf, bus_voltage, impedance, angle_rad):
    if abs(impedance) == 0:
        raise ValueError("nonzero impedance required")
    e = emf*np.exp(1j*np.asarray(angle_rad))
    current = (e-bus_voltage)/impedance
    return e*np.conj(current)

def lossless_synchronizing_gain(emf, voltage, reactance, angle_rad):
    if reactance <= 0:
        raise ValueError("positive reactance required")
    return emf*voltage*np.cos(angle_rad)/reactance
