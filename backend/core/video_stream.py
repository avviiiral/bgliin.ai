import cv2
import time

from core.camera_manager import LATEST_FRAMES, FRAME_LOCKS


def start_all_cameras():
    """
    Camera threads are now started by camera_manager/system_controller.
    This function is kept only so apps.py doesn't break.
    """
    print("[INFO] Using shared frames from camera_manager")


def generate_frames(cam_id):
    while True:

        if cam_id not in LATEST_FRAMES:
            time.sleep(0.05)
            continue

        try:
            with FRAME_LOCKS[cam_id]:
                frame = LATEST_FRAMES[cam_id].copy()
        except Exception:
            time.sleep(0.01)
            continue

        success, buffer = cv2.imencode(
            ".jpg",
            frame,
            [int(cv2.IMWRITE_JPEG_QUALITY), 80]
        )

        if not success:
            continue

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            buffer.tobytes() +
            b'\r\n'
        )

        time.sleep(0.01)