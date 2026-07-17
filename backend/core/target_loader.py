from datetime import datetime, timedelta

from django.db.utils import OperationalError, ProgrammingError

from apps.analytics.models import CameraTarget, ShiftSettings


def _shift_hours():

    try:
        shift = ShiftSettings.objects.first()

        if shift is None:
            return 0

        today = datetime.today()

        start = datetime.combine(today, shift.shift_start)
        end = datetime.combine(today, shift.shift_end)

        if end <= start:
            end += timedelta(days=1)

        return (end - start).total_seconds() / 3600

    except (OperationalError, ProgrammingError):
        # Database/table doesn't exist yet
        return 0


def load_targets():

    targets = {}

    try:

        shift_hours = _shift_hours()

        for cam in CameraTarget.objects.all():

            target_per_hour = 3600 / cam.cycle_time

            targets[cam.camera_id] = int(target_per_hour)

    except (OperationalError, ProgrammingError):
        # Database/tables don't exist yet
        return {}

    return targets


# Safe to import before migrations
TARGETS = {}