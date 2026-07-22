from django.urls import path
from .views import camera_list, all_stats, camera_stats, video_feed, camera_snapshot

urlpatterns = [
    path('cameras/', camera_list),
    path('stats/', all_stats),
    path('stats/<str:camera_id>/', camera_stats),
    path('video_feed/<str:cam_id>/', video_feed),
    path('video_feed', video_feed),
    path('snapshot/<str:cam_id>/', camera_snapshot),
]