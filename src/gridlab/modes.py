"""Eigenvalue diagnostics; neutral modes are reported separately from stable modes."""

import numpy as np


def modes(matrix, neutral_tolerance=1e-7):
    a = np.asarray(matrix, float)
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("square state matrix required")
    values = np.linalg.eigvals(a)
    return [
        {
            "real": float(v.real),
            "imag": float(v.imag),
            "frequency_hz": float(abs(v.imag) / (2 * np.pi)),
            "damping_ratio": None if abs(v) <= neutral_tolerance else float(-v.real / abs(v)),
            "classification": (
                "neutral" if abs(v.real) <= neutral_tolerance else "unstable" if v.real > 0 else "stable"
            ),
        }
        for v in sorted(values, key=lambda v: v.real, reverse=True)
    ]


def spectral_abscissa(matrix, exclude_neutral=True, tolerance=1e-7):
    eigen = np.linalg.eigvals(matrix)
    selected = eigen[abs(eigen.real) > tolerance] if exclude_neutral else eigen
    return None if len(selected) == 0 else float(max(selected.real))
