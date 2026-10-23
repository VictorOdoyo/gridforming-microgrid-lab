"""Long-form CSV with explicit quantity names and units."""
import csv
from pathlib import Path
import numpy as np

def export_csv(result, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["time_s", "entity", "quantity", "value", "unit"])
        for k, time in enumerate(result.time):
            for bus, voltage in enumerate(result.voltage[k]):
                writer.writerow([time, f"bus-{bus}", "voltage_magnitude", abs(voltage), "pu"])
                writer.writerow([time, f"bus-{bus}", "voltage_angle", np.angle(voltage), "rad"])
            for i, name in enumerate(result.source_names):
                writer.writerow([time, name, "connected", int(result.enabled[k, i]), "bool"])
                if result.enabled[k, i]:
                    writer.writerow([time, name, "internal_frequency", result.frequency_hz[k, i], "Hz"])
                writer.writerow([time, name, "active_power", result.power[k, i].real, "pu"])
                writer.writerow([time, name, "reactive_power", result.power[k, i].imag, "pu"])
                writer.writerow([time, name, "current_magnitude", abs(result.current[k, i]), "pu"])
    return path
