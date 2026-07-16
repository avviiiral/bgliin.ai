import multiprocessing as mp
import time
from .config import CAMERAS
from camera_manager import capture_worker
from inference import inference_worker
from csv_writer import init_csv, csv_logger


def start():

    mp.set_start_method("spawn")

    manager = mp.Manager()
    shared_counts = manager.dict({cid: 0 for cid in CAMERAS})
    reset_flag = manager.Value('i', 0)

    frame_queues = {cid: mp.Queue(maxsize=5) for cid in CAMERAS}

    # capture
    for cam_id, cam_cfg in CAMERAS.items():
        mp.Process(target=capture_worker, args=(cam_id, cam_cfg, frame_queues[cam_id]), daemon=True).start()

    # inference
    mp.Process(target=inference_worker, args=(frame_queues, shared_counts, reset_flag), daemon=True).start()

    # csv
    init_csv()
    mp.Process(target=csv_logger, args=(shared_counts, reset_flag), daemon=True).start()

    print("Core running")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    start()