"""Average alpha-beta voltage synthesis; no switching harmonics are synthesized."""
import numpy as np

def limit_vector(vector, maximum):
    if maximum < 0 or not np.isfinite(maximum):
        raise ValueError("maximum must be finite and nonnegative")
    value = np.asarray(vector, complex)
    scale = np.minimum(1, np.divide(maximum, np.maximum(abs(value), 1e-30)))
    return value*scale

def voltage_command(requested_peak, dc_voltage, method="svpwm"):
    if dc_voltage < 0:
        raise ValueError("DC voltage must be nonnegative")
    if method not in ("svpwm", "sinusoidal"):
        raise ValueError("unknown modulation method")
    maximum = dc_voltage/(np.sqrt(3) if method == "svpwm" else 2)
    return limit_vector(requested_peak, maximum)
