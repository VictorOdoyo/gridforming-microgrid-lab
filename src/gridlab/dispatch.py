"""Greedy dispatch experiment, independent of the fast phasor dynamics."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Dispatch:
    solar_kw: float
    battery_kw: float
    diesel_kw: float
    curtailed_kw: float
    unmet_kw: float
    soc: float

def dispatch(load_kw, solar_kw, battery, soc, diesel_rating_kw, dt_s):
    if min(load_kw, solar_kw, diesel_rating_kw) < 0:
        raise ValueError("loads and ratings must be nonnegative")
    deficit = load_kw-solar_kw
    next_soc, batt = battery.step(soc, deficit, dt_s)
    remaining = deficit-batt
    diesel = min(diesel_rating_kw, max(0, remaining))
    curtailed = max(0, -remaining)
    unmet = max(0, remaining-diesel)
    return Dispatch(solar_kw-curtailed, batt, diesel, curtailed, unmet, next_soc)
