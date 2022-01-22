import hashlib
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
        """Get timezone with Django"""

        return timezone.now()

    @staticmethod
    def date_is_future(date):
        """Get timezone with Django"""

        return date > timezone.now()

    @staticmethod
    def hash_string(string: str):
        """Hash string with SHA384"""

        hash_object = hashlib.sha384(string.encode('utf-8'))
        return hash_object.hexdigest()

    @staticmethod
    def hash_string_ip(string: str):
        """Hash string with SHA384 and return 30 characters"""

        hash_object = hashlib.sha384(string.encode('utf-8'))
        return hash_object.hexdigest()[:30]

    @staticmethod
    def get_client_ip(request):
        """Get client IP from request context object"""

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
