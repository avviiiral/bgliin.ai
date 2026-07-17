import csv
import os
from core.config import CSV_FILE, CAMERAS
#from .views import camera_dashboard
from datetime import datetime, timedelta
from apps.analytics.models import ShiftSettings

def get_shift():
    shift = ShiftSettings.objects.first()

    if shift is None:
        from datetime import time
        return time(0, 0), time(23, 59)

    return shift.shift_start, shift.shift_end

def read_csv():
    if not os.path.exists(CSV_FILE):
        return []

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def validate_column(camera_name, data):
    if not data:
        return False

    if camera_name not in data[0]:
        print(f"[ERROR] Column '{camera_name}' not found in CSV")
        return False

    return True


def get_camera_history(camera_name):
    data = read_csv()

    if not validate_column(camera_name, data):
        return []

    history = []

    for row in data:
        try:
            val = row[camera_name]

            if val == "":
                continue

            history.append({
                "datetime": f"{row['Date']} {row['Time Slot']}",
                "count": float(val)
            })
        except:
            continue

    return history


def compute_production(camera_name):
    history = get_camera_history(camera_name)

    return [
        {
            "time": h["datetime"],
            "production": h["count"]
        }
        for h in history
    ]


def compute_efficiency(camera_name, target=100):
    history = get_camera_history(camera_name)

    result = []

    for h in history:
        actual = h["count"]
        efficiency = (actual / target) * 100 if target else 0

        result.append({
            "time": h["datetime"],
            "actual": actual,
            "target": target,
            "efficiency": round(efficiency, 2)
        })

    return result

def get_shift_elapsed_seconds(now=None):
    
    SHIFT_START, SHIFT_END = get_shift()

    if SHIFT_START is None:
        return 0

    if now is None:
        now = datetime.now()

    today = now.date()

    shift_start_dt = datetime.combine(today, SHIFT_START)
    shift_end_dt = datetime.combine(today, SHIFT_END)

    if SHIFT_END < SHIFT_START:
        if now.time() < SHIFT_END:
            shift_start_dt -= timedelta(days=1)
        else:
            shift_end_dt += timedelta(days=1)

    if now < shift_start_dt:
        return 0

    if now > shift_end_dt:
        return (shift_end_dt - shift_start_dt).total_seconds()

    return (now - shift_start_dt).total_seconds()


def get_shift_elapsed_hours(now=None):
    return get_shift_elapsed_seconds(now) / 3600


def is_time_in_shift(timeslot):
    
    SHIFT_START, SHIFT_END = get_shift()

    if SHIFT_START is None:
        return False

    try:
        hour = int(timeslot.split(":")[0])
    except:
        return False

    if SHIFT_START.hour <= SHIFT_END.hour:
        return SHIFT_START.hour <= hour <= SHIFT_END.hour

    return hour >= SHIFT_START.hour or hour <= SHIFT_END.hour


def compute_downtime_from_df(df, column):
    downtime_minutes = 0
    total_minutes = 0

    for _, row in df.iterrows():
        timeslot = row["Time Slot"]

        if not is_time_in_shift(timeslot):
            continue

        value = row[column]

        # each row = 60 minutes (your CSV is hourly)
        total_minutes += 60

        if int(value) == 0:
            downtime_minutes += 60

    uptime_minutes = total_minutes - downtime_minutes

    downtime_percent = (downtime_minutes / total_minutes * 100) if total_minutes > 0 else 0

    return {
        "downtime_minutes": downtime_minutes,
        "uptime_minutes": uptime_minutes,
        "downtime_percent": round(downtime_percent, 2)
    }