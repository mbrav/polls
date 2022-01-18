from rest_framework import serializers

from .models import Choice, Poll, Vote


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Base Choice serializer
    """

    class Meta:
        model = Choice
        fields = ['text']


class VoteSerializer(serializers.ModelSerializer):
    """
    Base Vote serializer
    """
    vote_count = serializers.SerializerMethodField(
        method_name='get_vote_count')

    def get_vote_count(self, obj):
        return obj.vote.count()

    class Meta:
        model = Vote
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    """
    Base Poll serializer
    """

    choices = ChoiceSerializer(
        source='choice',
        read_only=True,
        many=True
    )

    vote_count = serializers.SerializerMethodField(
        method_name='get_vote_count')

    def get_vote_count(self, obj):
        return obj.vote.count()

    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'is_open',
            'vote_count', 'choices', 'date_created', 'date_end']
