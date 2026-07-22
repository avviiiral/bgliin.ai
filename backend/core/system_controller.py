import multiprocessing as mp
import threading
import time
from core.logger import logger

from core.config import CAMERAS
from core.camera_manager import capture_worker
from core.inference import inference_worker
from core.csv_writer import init_csv, csv_logger

manager = None
shared_counts = None
reset_flag = None
frame_queues = None

# 🔥 store full process metadata (IMPORTANT)
processes = []


def start_system():
    global manager, shared_counts, reset_flag, frame_queues, processes

    if manager is not None:
        print("System already running")
        return

    mp.set_start_method("spawn", force=True)

    manager = mp.Manager()
    shared_counts = manager.dict({cid: 0 for cid in CAMERAS})
    reset_flag = manager.Value('i', 0)

    frame_queues = {cid: mp.Queue(maxsize=5) for cid in CAMERAS}

    processes = []

    # ==============================
    # CAPTURE PROCESSES
    # ==============================
    # CAPTURE THREADS
    for cam_id, cam_cfg in CAMERAS.items():
        t = threading.Thread(
            target=capture_worker,
            args=(cam_id, cam_cfg, frame_queues[cam_id]),
            daemon=True
        )
        t.start()
    # ==============================
    # INFERENCE PROCESS
    # ==============================
    p = mp.Process(
        target=inference_worker,
        args=(frame_queues, shared_counts, reset_flag)
    )
    p.daemon = True
    p.start()

    processes.append({
        "process": p,
        "target": inference_worker,
        "args": (frame_queues, shared_counts, reset_flag)
    })

    # ==============================
    # CSV LOGGER PROCESS
    # ==============================
    init_csv()

    p = mp.Process(
        target=csv_logger,
        args=(shared_counts, reset_flag)
    )
    p.daemon = True
    p.start()

    processes.append({
        "process": p,
        "target": csv_logger,
        "args": (shared_counts, reset_flag)
    })

    # ==============================
    # MONITOR THREAD
    # ==============================

    logger.info(" Core system started")
    print(" Core system started")


# ==============================
# GET COUNTS (API USE)
# ==============================
def get_counts():
    if shared_counts is None:
        return {}
    return dict(shared_counts)


# ==============================
# PROCESS MONITOR (FIXED)
# ==============================
def monitor_processes():
    global processes

    while True:
        for i, p_data in enumerate(processes):
            p = p_data["process"]

            if not p.is_alive():
                print(f"[ERROR] Process {i} died. Restarting...")

                new_p = mp.Process(
                    target=p_data["target"],
                    args=p_data["args"]
                )
                new_p.daemon = True
                new_p.start()

                processes[i]["process"] = new_p

        time.sleep(5)