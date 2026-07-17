from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .utils import compute_downtime_from_df, get_shift_elapsed_hours

from core.target_loader import load_targets  # ✅ FIXED

import pandas as pd
import os


# ===================== CONFIG =====================

CSV_PATH = os.path.join(settings.BASE_DIR, "production_hourly.csv")

COLUMN_TO_CAMERA = {
    "AIR WASHING": "cam1",
    "MIDDLE TESTING": "cam2",
    "COIL SOLDERING": "cam3",
    "FRAME CRIMPING": "cam4",
    "COMMON CRIMPING": "cam5",
    "WIRE ROUTING": "cam6",
    "BASE ASSEMBLY": "cam7",
    "M SPRING RIVETTING": "cam8",
    "CORE RIVETTING": "cam9",
    "BOBBIN PRESSING": "cam10"
}


# ===================== UTIL =====================

def load_csv():
    if not os.path.exists(CSV_PATH):
        return None

    df = pd.read_csv(CSV_PATH, low_memory=False)
    df.columns = [c.strip() for c in df.columns]

    if "Date" not in df.columns or "Time Slot" not in df.columns:
        return None

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by=["Date", "Time Slot"])

    return df


def get_column_from_camera(camera_id):
    for col, cam in COLUMN_TO_CAMERA.items():
        if cam == camera_id:
            return col
    return None


# ===================== DASHBOARD =====================

@api_view(['GET'])
def dashboard_summary(request):
    df = load_csv()
    TARGETS = load_targets()  # ✅ dynamic

    if df is None:
        return Response({"error": "CSV not found"}, status=404)

    production_df = df.iloc[:, 2:]

    latest_row = production_df.iloc[-1]
    total_output = int(latest_row.sum())

    total_target = int(sum(TARGETS.values()))

    station_totals = production_df.sum()

    active_stations = int((latest_row > 0).sum())
    total_stations = len(station_totals)

    efficiency = (total_output / total_target * 100) if total_target > 0 else 0

    return Response({
        "efficiency": round(efficiency, 1),
        "output": total_output,
        "target": total_target,
        "active_stations": active_stations,
        "total_stations": total_stations,

        "per_station": latest_row.to_dict(),
        "per_station_targets": TARGETS,

        "status": "All systems operational" if active_stations == total_stations else "Some stations idle"
    })


# ===================== STATIONS =====================

@api_view(['GET'])
def stations(request):
    df = load_csv()
    TARGETS = load_targets()  # ✅ dynamic

    if df is None:
        return Response({"error": "CSV not found"}, status=404)

    production_df = df.iloc[:, 2:]
    station_totals = production_df.sum()

    latest_row = df.iloc[-1]
    elapsed_hours = get_shift_elapsed_hours()

    result = []

    for column_name, total in station_totals.items():
        cam_id = COLUMN_TO_CAMERA.get(column_name)

        if not cam_id:
            continue

        target_per_hour = TARGETS.get(cam_id, 0)
        target_total = target_per_hour * elapsed_hours

        efficiency = (total / target_total * 100) if target_total > 0 else 0
        latest_output = int(latest_row.loc[column_name])

        result.append({
            "camera_id": cam_id,
            "name": column_name,
            "output": int(total),
            "target": target_total,
            "efficiency": round(efficiency, 1),
            "status": "active" if total > 0 else "idle",
            "latest_output": latest_output,
            "is_live": True
        })

    return Response(result)


# ===================== CAMERA DETAIL =====================

@api_view(['GET'])
def camera_detail(request, camera_id):
    df = load_csv()
    TARGETS = load_targets()  # ✅ dynamic

    if df is None:
        return Response({"error": "CSV not found"}, status=404)

    column = get_column_from_camera(camera_id)

    if not column or column not in df.columns:
        return Response({"error": "Invalid camera"}, status=404)

    selected_date = request.GET.get("date")

    if selected_date:
        selected_date = pd.to_datetime(selected_date)
        df_filtered = df[df["Date"] == selected_date]
    else:
        df_filtered = df[df["Date"] == df["Date"].max()]

    if df_filtered.empty:
        return Response({"error": "No data for selected date"}, status=404)

    target_per_hour = TARGETS.get(camera_id, 0)

    total_output = int(df_filtered[column].sum())

    elapsed_hours = get_shift_elapsed_hours()
    total_target = target_per_hour * elapsed_hours

    efficiency = (total_output / total_target * 100) if total_target > 0 else 0

    hourly_output = [
        {
            "time": row["Time Slot"],
            "output": int(row[column])
        }
        for _, row in df_filtered.iterrows()
    ]

    pph = (total_output / elapsed_hours) if elapsed_hours > 0 else 0
    avg_cycle_time = (3600 / pph) if pph > 0 else 0

    expected = target_per_hour * elapsed_hours
    pieces_ahead = total_output - expected

    downtime_data = compute_downtime_from_df(df_filtered, column)

    return Response({
        "camera_id": camera_id,
        "name": column,
        "date": str(df_filtered["Date"].iloc[0].date()),

        "output": total_output,
        "target": total_target,
        "target_per_hour": target_per_hour,
        "efficiency": round(efficiency, 1),

        "hourly_output": hourly_output,

        "pph": round(pph, 1),
        "avg_cycle_time": round(avg_cycle_time, 2),
        "pieces_ahead": int(pieces_ahead),

        "downtime_minutes": downtime_data["downtime_minutes"],
        "uptime_minutes": downtime_data["uptime_minutes"],
        "downtime_percent": downtime_data["downtime_percent"]
    })


# ===================== CALENDAR =====================

@api_view(['GET'])
def camera_calendar(request, camera_id):
    df = load_csv()
    TARGETS = load_targets()  # ✅ dynamic

    if df is None:
        return Response({"error": "CSV not found"}, status=404)

    column = get_column_from_camera(camera_id)

    if not column:
        return Response({"error": "Invalid camera"}, status=404)

    grouped = df.groupby("Date")
    target_per_hour = TARGETS.get(camera_id, 0)

    result = []

    for date, group in grouped:
        output = group[column].sum()
        hours = len(group)

        target = target_per_hour * hours
        efficiency = (output / target * 100) if target > 0 else 0

        if efficiency >= 80:
            status = "good"
        elif efficiency >= 60:
            status = "average"
        else:
            status = "poor"

        result.append({
            "date": str(pd.Timestamp(date).date()),
            "output": int(output),
            "efficiency": round(efficiency, 1),
            "status": status
        })

    result = sorted(result, key=lambda x: x["date"])

    return Response(result)


# ===================== HISTORY =====================

@api_view(['GET'])
def camera_history(request, camera_id):
    df = load_csv()

    if df is None:
        return Response({"error": "CSV not found"}, status=404)

    column = get_column_from_camera(camera_id)

    if not column:
        return Response({"error": "Invalid camera"}, status=404)

    history = []

    for _, row in df.iterrows():
        history.append({
            "time": f"{row['Date'].date()} {row['Time Slot']}",
            "output": int(row[column])
        })

    return Response(history)


# ===================== STATION DASHBOARD =====================

@api_view(['GET'])
def station_dashboard(request, station_name):
    import csv
    from core.config import CSV_FILE
    from core.target_loader import load_targets

    TARGETS = load_targets()  # ✅ dynamic

    hourly_output = []
    total_output = 0

    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            count = int(row[station_name])

            hourly_output.append({
                "hour": row["Time Slot"],
                "count": count
            })

            total_output += count

    target_per_hour = TARGETS.get(station_name, 400)

    elapsed_hours = get_shift_elapsed_hours()
    expected_total = target_per_hour * elapsed_hours

    efficiency = (total_output / expected_total) * 100 if expected_total else 0

    return Response({
        "station": station_name,
        "total_output": total_output,
        "hourly_output": hourly_output,
        "efficiency": round(efficiency, 2),
        "target_per_hour": target_per_hour
    })

@api_view(['GET'])
def monthly_history(request, camera_id):

    df = load_csv()
    TARGETS = load_targets()

    if df is None:
        return Response({"error": "CSV not found"}, status=404)

    column = get_column_from_camera(camera_id)

    if not column:
        return Response({"error": "Invalid camera"}, status=404)

    year = int(request.GET.get("year"))
    month = int(request.GET.get("month"))

    # Filter by year/month
    df = df[
        (df["Date"].dt.year == year) &
        (df["Date"].dt.month == month)
    ]

    grouped = df.groupby(df["Date"].dt.day)

    result = []

    target_per_hour = TARGETS.get(camera_id, 100)

    for day, group in grouped:

        output = int(group[column].sum())

        hours = len(group)

        target = target_per_hour * hours

        efficiency = (output / target * 100) if target > 0 else 0

        # Calendar color logic
        if efficiency >= 90:
            status = "green"
        elif efficiency >= 70:
            status = "yellow"
        else:
            status = "red"

        result.append({
            "day": int(day),
            "count": output,
            "target": target,
            "efficiency": round(efficiency, 1),
            "status": status
        })

    return Response(result)
