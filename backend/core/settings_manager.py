from datetime import datetime, timedelta
from apps.analytics.models import ProductionSettings


def get_settings():
    return ProductionSettings.objects.first()


def is_shift_running():

    settings = get_settings()

    if not settings:
        return False

    now = datetime.now().time()

    start = settings.shift_start
    end = settings.shift_end

    if start <= end:
        return start <= now <= end

    return now >= start or now <= end


def get_target():

    settings = get_settings()

    if settings:
        return settings.target()

    return 0


def get_cycle_time():

    settings = get_settings()

    if settings:
        return settings.cycle_time

    return None