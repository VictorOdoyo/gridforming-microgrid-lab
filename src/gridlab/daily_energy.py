"""Slow energy dispatch experiment; separate from fast AC outer-loop dynamics."""
import numpy as np
from .battery import Battery
from .solar import PVArray
from .dispatch import dispatch

def daily_energy(step_s=300.0, initial_soc=.5):
    if not np.isfinite(step_s) or not 0 < step_s <= 3600:
        raise ValueError("step must be between zero and one hour")
    battery = Battery(120, 40, 40)
    solar = PVArray(100)
    soc, records = initial_soc, []
    for time in np.arange(0, 86400, step_s):
        dt = min(step_s, 86400-time)
        hour = (time+dt/2)/3600
        irradiance = 900*max(0, np.sin(np.pi*(hour-6)/12)) if 6 <= hour <= 18 else 0
        load = 30+15*np.exp(-((hour-19)/3)**2)+5*np.exp(-((hour-8)/2)**2)
        available = float(solar.available_kw(irradiance, 25))
        d = dispatch(load, available, battery, soc, 60, dt)
        soc = d.soc
        records.append({"time_s": float(time), "interval_s": float(dt), "load_kw": float(load),
                        "available_solar_kw": available, "solar_kw": d.solar_kw,
                        "battery_kw": d.battery_kw, "diesel_kw": d.diesel_kw,
                        "curtailed_kw": d.curtailed_kw, "unmet_kw": d.unmet_kw, "soc": soc})
    totals = {key.replace("_kw", "_kwh"): sum(r[key]*r["interval_s"]/3600 for r in records)
              for key in ("load_kw", "solar_kw", "diesel_kw", "curtailed_kw", "unmet_kw")}
    totals.update(initial_soc=initial_soc, final_soc=soc,
                  minimum_soc=min(initial_soc, *(r["soc"] for r in records)),
                  maximum_soc=max(initial_soc, *(r["soc"] for r in records)))
    return {"summary": totals, "intervals": records}
