import os
from django.apps import AppConfig

_started = False
class CamerasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cameras'

    

    def ready(self):
        global _started

        if _started:
            return

        _started = True

        print("🚀 Starting camera threads...")

        from core.video_stream import start_all_cameras
        start_all_cameras()

        from core.system_controller import start_system
        start_system()