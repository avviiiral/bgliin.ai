from datetime import datetime
import time as tm
from ultralytics import YOLO

from core.config import *
from core.counter import Counter
from core.logger import logger
from core.utils import is_within_shift


def inference_worker(frame_queues, shared_counts, reset_flag):

    model = YOLO(MODEL_PATH)
    model.to(DEVICE)

    logger.info(f"YOLO model loaded on {DEVICE}")

    counters = {
        cid: Counter(cfg, cid)
        for cid, cfg in CAMERAS.items()
    }

    while True:

        # Shift check
        if not is_within_shift():

            # Drain old frames
            for q in frame_queues.values():
                while not q.empty():
                    try:
                        q.get_nowait()
                    except:
                        break

            tm.sleep(0.01)
            continue

        batch_frames = []
        batch_meta = []

        # Collect frames
        for cam_id, q in frame_queues.items():

            if not q.empty():

                try:
                    cid, frame = q.get_nowait()

                    batch_frames.append(frame)
                    batch_meta.append(cid)

                except:
                    continue

            if len(batch_frames) >= BATCH_SIZE:
                break

        # No frames
        if not batch_frames:
            tm.sleep(0.01)
            continue

        # YOLO inference
        results = model(
            batch_frames,
            conf=0.3,
            device=DEVICE,
            verbose=False
        )

        # Process detections
        for i, r in enumerate(results):

            cam_id = batch_meta[i]

            centers = []

            if r.boxes is not None:

                boxes = r.boxes.xyxy.cpu().numpy()

                for box in boxes:

                    x1, y1, x2, y2 = map(int, box)

                    centers.append((
                        (x1 + x2) // 2,
                        (y1 + y2) // 2
                    ))

            counters[cam_id].update(centers)

            shared_counts[cam_id] = counters[cam_id].count