"""Amplitude-invariant transforms with explicit zero sequence."""
import numpy as np

_CLARKE = np.array([[2/3, -1/3, -1/3],
                    [0, 1/np.sqrt(3), -1/np.sqrt(3)],
                    [1/3, 1/3, 1/3]])

def clarke(abc):
    return np.asarray(abc) @ _CLARKE.T

def inverse_clarke(ab0):
    return np.asarray(ab0) @ np.linalg.inv(_CLARKE).T

def park(ab0, angle):
    a, b, z = np.moveaxis(np.asarray(ab0), -1, 0)
    c, s = np.cos(angle), np.sin(angle)
    return np.stack((a*c + b*s, -a*s + b*c, z), axis=-1)

def inverse_park(dq0, angle):
    return park(dq0, -np.asarray(angle))
