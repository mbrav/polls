from datetime import timedelta

from django.utils import timezone


class Util:
    """Utilities for Polls project"""

    @staticmethod
    def close_date(days: int = 30):
        return timezone.now() + timedelta(days=int(days))

    @staticmethod
    def time_now():
        return timezone.now()
