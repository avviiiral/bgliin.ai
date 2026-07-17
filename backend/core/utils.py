from datetime import datetime
from django.apps import apps


def is_within_shift():
    try:
        ShiftSettings = apps.get_model("analytics", "ShiftSettings")
    except Exception:
        return True

    settings = ShiftSettings.objects.first()

    if settings is None:
        return True

    now = datetime.now().time()

    start = settings.shift_start
    end = settings.shift_end

    if start < end:
        return start <= now <= end

    return now >= start or now <= end