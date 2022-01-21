from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Choice, Poll, Vote
from .utils import Util


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Base Choice serializer
    """

    count = serializers.SerializerMethodField(
        method_name='get_vote_count')

    count_percent = serializers.SerializerMethodField(
        method_name='get_vote_percent')

    def get_vote_count(self, obj):
        return obj.vote.count()

    def get_vote_percent(self, obj):
        total_vote_count = obj.poll.vote.count()
        try:
            return obj.vote.count() / total_vote_count * 100
        except ZeroDivisionError:
            return 0

    class Meta:
        model = Choice
        fields = ('id', 'text', 'count', 'count_percent')


class VoteSerializer(serializers.ModelSerializer):
    """
    Base Vote serializer
    """

    def validate(self, attrs):
        poll = attrs.get('poll', None)
        choice = attrs.get('choice', None)
        user = attrs.get('user', None)

        if poll.date_end < Util.time_now():
            raise serializers.ValidationError(
                'Sorry, Poll\'s voting period has expired')

        poll_has_choice = Choice.objects.filter(poll=poll).exists()
        user_has_voted = Vote.objects.filter(poll=poll, user=user).exists()

        if not poll_has_choice:
            raise serializers.ValidationError(
                f'Poll \'{poll.name}\' does not have \'{choice.text}\' as option')

        if user_has_voted:
            raise serializers.ValidationError(
                f'Sorry, you already casted your vote in poll \'{poll.name}\'')

        return attrs

    class Meta:
        model = Vote
        fields = '__all__'
        # read_only_fields = ('user',)


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
        read_only=True,
        method_name='get_vote_count')

    def get_vote_count(self, obj):
        return obj.vote.count()

    class Meta:
        model = Poll
        fields = ('id', 'name', 'description', 'is_open',
            'vote_count', 'choices', 'date_created', 'date_end')


class PollSerializerClose(serializers.ModelSerializer):
    """
    Poll serializer for Closing Poll
    """

    date_end = serializers.DateTimeField(required=False)

    def validate_date_end(self, value):
        poll_pk = self.context['view'].kwargs.get('pk')
        poll = Poll.objects.get(pk=poll_pk)
        if value < poll.date_created:
            raise serializers.ValidationError(
                'date_end cannot be prior to date_created')
        return value

    class Meta:
        model = Poll
        fields = ('date_end',)


class PollSerializerExtend(PollSerializerClose):
    """
    Poll serializer for Extending Poll
    """

    minutes = serializers.IntegerField(
        write_only=True,
        default=0,
        required=False)

    hours = serializers.IntegerField(
        write_only=True,
        default=0,
        required=False)

    days = serializers.IntegerField(
        write_only=True,
        default=0,
        required=False)

    weeks = serializers.IntegerField(
        write_only=True,
        default=0,
        required=False)

    def validate(self, attrs):
        # fields = tuple(self.fields)
        if len(attrs) == 0:
            raise serializers.ValidationError(
                'Please provide date_end or one of four time increments')
        return attrs

    class Meta:
        model = Poll
        fields = ('date_end', 'minutes', 'hours', 'days', 'weeks')
