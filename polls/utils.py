from datetime import timedelta

from django.utils import timezone


class Util:
    """Utilities for Polls project"""

    @staticmethod
    def close_date(date=None, *args, **kwargs):
        """Get date based on provided arguments 
        inherited from datetime.timedelta:

        days=0
        seconds=0
        microseconds=0
        milliseconds=0
        minutes=0
        hours=0
        weeks=0
        """

        # Convert to int
        for key, value in kwargs.items():
            kwargs[key] = int(value)

        if date:
            return date + timedelta(**kwargs)
        return timezone.now() + timedelta(**kwargs)

    @staticmethod
    def time_now():
        return timezone.now()
