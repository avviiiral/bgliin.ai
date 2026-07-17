from django.db import models


class ShiftSettings(models.Model):
    shift_start = models.TimeField()
    shift_end = models.TimeField()

    def __str__(self):
        return "Shift Settings"


class CameraTarget(models.Model):
    camera_id = models.CharField(max_length=20, unique=True)
    camera_name = models.CharField(max_length=100)
    cycle_time = models.FloatField(help_text="Seconds per part")

    def __str__(self):
        return self.camera_name