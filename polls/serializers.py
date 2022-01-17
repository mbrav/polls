from rest_framework import serializers

from .models import Poll


class PollSerializer(serializers.ModelSerializer):
    """
    Base Poll serializer
    """

    class Meta:
        model = Poll
        fields = ('__all__',)
        # read_only_fields = ('height', 'width')

