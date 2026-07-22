from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.system_controller import get_counts
from core.config import CAMERAS

from django.http import StreamingHttpResponse, HttpResponse, HttpResponseNotFound
from core.video_stream import generate_frames
from core.camera_manager import LATEST_FRAMES, FRAME_LOCKS
import cv2

@api_view(['GET'])
def camera_list(request):
    return Response(CAMERAS)


@api_view(['GET'])
def all_stats(request):
    return Response(get_counts())


@api_view(['GET'])
def camera_stats(request, camera_id):
    counts = get_counts()

    return Response({
        "camera_id": camera_id,
        "count": counts.get(camera_id, 0)
    })


def video_feed(request, cam_id):
    return StreamingHttpResponse(
        generate_frames(cam_id),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


def camera_snapshot(request, cam_id):
    if cam_id not in LATEST_FRAMES:
        return HttpResponseNotFound('Camera not ready yet')

    try:
        with FRAME_LOCKS[cam_id]:
            frame = LATEST_FRAMES[cam_id].copy()
    except Exception:
        return HttpResponseNotFound('Camera not ready yet')

    success, buffer = cv2.imencode(
        '.jpg',
        frame,
        [int(cv2.IMWRITE_JPEG_QUALITY), 80]
    )

    if not success:
        return HttpResponseNotFound('Could not encode frame')

    response = HttpResponse(buffer.tobytes(), content_type='image/jpeg')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response