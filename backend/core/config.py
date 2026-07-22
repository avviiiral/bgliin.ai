import torch
from datetime import time

CAMERAS = {
    "cam1": {"ip": "192.168.1.193", "name": "AIR WASHING", "mode": "x", "pos": 1100, "dir": "lr", "multiplier": 1},
    "cam2": {"ip": "192.168.1.191", "name": "MIDDLE TESTING", "mode": "x", "pos": 1035, "dir": "lr", "multiplier": 1},
    "cam3": {"ip": "192.168.1.196", "name": "COIL SOLDERING", "mode": "x", "pos": 1000, "dir": "lr", "multiplier": 2},
    "cam4": {"ip": "192.168.1.198", "name": "FRAME CRIMPING", "mode": "x", "pos": 800, "dir": "rl", "multiplier": 1},
    "cam5": {"ip": "192.168.1.194", "name": "COMMON CRIMPING", "mode": "x", "pos": 800, "dir": "rl", "multiplier": 1},
    "cam6": {"ip": "192.168.1.197", "name": "WIRE ROUTING", "mode": "x", "pos": 870, "dir": "rl", "multiplier": 1},
    "cam7": {"ip": "192.168.1.188", "name": "BASE ASSEMBLY", "mode": "x", "pos": 1100, "dir": "lr", "multiplier": 1},
    "cam8": {"ip": "192.168.1.189", "name": "M SPRING RIVETTING", "mode": "x", "pos": 1200, "dir": "lr", "multiplier": 0.5},
    "cam9": {"ip": "192.168.1.190", "name": "CORE RIVETTING", "mode": "x", "pos": 1150, "dir": "lr", "multiplier": 0.5},
    "cam10": {"ip": "192.168.1.201", "name": "BOBBIN PRESSING", "mode": "x", "pos": 1100, "dir": "lr", "multiplier": 1},
}

USERNAME = "admin"
PASSWORD = "Admin%40123"

MODEL_PATH = r"C:\bagla\backend\model\best.pt"
FRAME_W, FRAME_H = 512, 288
ORIGINAL_W, ORIGINAL_H = 1920, 1080

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 8

MOVE_THRESH = 12
COOLDOWN = 20

CSV_FILE = "production_hourly.csv"

# ================= SHIFT CONFIG =================
SHIFT_ENABLED = True

# single shift
SHIFT_START = time(9, 0, 0)   # 09:00
SHIFT_END   = time(17, 30, 0)  # 17:30

# optional multi-shift (uncomment if needed)
# SHIFTS = [
#     (time(9, 0), time(13, 0)),
#     (time(14, 0), time(18, 0)),
# ]