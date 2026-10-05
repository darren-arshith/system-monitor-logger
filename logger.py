import csv
import time
from datetime import datetime

import psutil

#Piece 2: Settings
LOG_FILE = "system_log.csv"
INTERVAL_SECONDS = 5
NUM_READINGS = 12

#Piece 3: Read the CPU temperature
def get_cpu_temp():
    """Return CPU temperature in °C, or None if not available."""
    temps = psutil.sensors_temperatures()
    for name in ("coretemp", "k10temp", "cpu_thermal", "acpitz"):
        if name in temps and temps[name]:
            return temps[name][0].current
    return None

#Piece 4: Take one reading (the "sensor" part)
def get_reading():
    """Take one snapshot of the system's current state."""
    battery = psutil.sensors_battery()
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent,
        "cpu_temp_c": get_cpu_temp(),
        "battery_percent":min(round(battery.percent,1),100) if battery else None,
        "plugged_in": battery.power_plugged if battery else None,
}

#Piece 5: Repeat and save to the file
def main():
    with open(LOG_FILE, "w", newline="") as f:
        writer = None
        for i in range(NUM_READINGS):
            reading = get_reading()
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=reading.keys())
                writer.writeheader()
            writer.writerow(reading)
            f.flush()
            print(f"[{i + 1}/{NUM_READINGS}] {reading}")
            time.sleep(INTERVAL_SECONDS)
    print(f"Done. Data saved to {LOG_FILE}")

#Piece 6: Start the program
if __name__=="__main__":
	main()
