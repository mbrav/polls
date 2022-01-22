from rest_framework import serializers

from .models import AnonUser, Choice, Poll, Vote
from .utils import Util


class AnonTokenSerializer(serializers.ModelSerializer):
    """
    AnonToken validation serializer based on client IP
    """

    ip_address = serializers.IPAddressField(
        read_only=True
    )

    token = serializers.CharField(
        read_only=True
    )

    def validate(self, attrs):
        request = self.context.get('request')
        ip = Util.get_client_ip(request)

        if not ip:
            msg = 'Unable to validate based on your IP address'
            raise serializers.ValidationError(msg, code='authorization')

        hashed_ip = Util.hash_string_ip(ip)
        user, created = AnonUser.objects.get_or_create(
            ip_address=ip, username=hashed_ip, is_active=True)

        attrs['ip_address'] = ip
        attrs['user'] = user
        return attrs

    class Meta:
        model = AnonUser
        fields = ('ip_address', 'token',)


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
        read_only_fields = ('count', 'count_percent', 'id')


class VoteSerializer(serializers.ModelSerializer):
    """
    Base Vote serializer
    """

    user = serializers.CharField(
        source='user.username',
        read_only=True,
    )

    def validate(self, attrs):
        poll = attrs.get('poll', None)
        choice = attrs.get('choice', None)

        if not poll:
            poll = self.instance.poll

        if not choice:
            choice = self.instance.choice

        user = self.context['request'].user

        if poll.date_end < Util.time_now():
            msg = 'Sorry, Poll\'s voting period has expired'
            raise serializers.ValidationError(msg)

        poll_has_choice = Choice.objects.filter(poll=poll).exists()
        user_has_voted = Vote.objects.filter(poll=poll, user=user).exists()
        same_vote = Vote.objects.filter(
            poll=poll, user=user, choice=choice).exists()

        if not poll_has_choice:
            msg = f'Poll \'{poll.name}\' does not have \'{choice.text}\' as option'
            raise serializers.ValidationError(msg)

        if same_vote:
            msg = 'You cannot vote for the same option more than once'
            raise serializers.ValidationError(msg)

        if user_has_voted and poll.type != '2':
            msg = f'Sorry, poll \'{poll.name}\' is not multivote'
            raise serializers.ValidationError(msg)

        return attrs

    class Meta:
        model = Vote
        fields = ('id', 'poll', 'choice', 'user')


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
        method_name='get_vote_count'
    )

    def get_vote_count(self, obj):
        return obj.vote.count()

    class Meta:
        model = Poll
        fields = ('id', 'name', 'type', 'description', 'is_open',
            'vote_count', 'choices', 'date_created', 'date_end')


class PollCloseSerializer(serializers.ModelSerializer):
    """
    Poll serializer for close @action
    """

    date_end = serializers.DateTimeField(required=False)
    is_open = serializers.BooleanField(
        read_only=True,
    )

    def validate_date_end(self, value):
        poll_pk = self.context['view'].kwargs.get('pk')
        poll = Poll.objects.get(pk=poll_pk)
        if value < poll.date_created:
            msg = 'date_end cannot be prior to date_created'
            raise serializers.ValidationError(msg)
        return value

    class Meta:
        model = Poll
        fields = ('date_end', 'is_open')


class PollExtendSerializer(PollCloseSerializer):
    """
    Poll serializer for extend @action
    """

    minutes = serializers.IntegerField(
        write_only=True,
        default=0,
        required=False
    )

    hours = serializers.IntegerField(
        write_only=True,
        default=0,
        required=False
    )

    days = serializers.IntegerField(
        write_only=True,
        default=0,
        required=False
    )

    weeks = serializers.IntegerField(
        write_only=True,
        default=0,
        required=False
    )

    def validate(self, attrs):
        # fields = tuple(self.fields)
        if len(attrs) == 0:
            msg = 'Please provide date_end or one of four time increments'
            raise serializers.ValidationError(msg)
        return attrs

    class Meta:
        model = Poll
        fields = ('date_end', 'minutes', 'hours', 'days', 'weeks', 'is_open')


class PollAddChoiceSerializer(PollCloseSerializer):
    """
    Serializer for add_choice @action
    """

    choice = serializers.CharField(
        write_only=True,
        required=True
    )

    def validate_choice(self, value):
        poll = self.instance

        if poll.type not in ('1', '2'):
            msg = 'Poll is not of a choice type'
            raise serializers.ValidationError(msg)

        choice_exists = Choice.objects.filter(
            text=value, poll=poll).exists()
        # fields = tuple(self.fields)
        if choice_exists:
            msg = 'Choice already exists'
            raise serializers.ValidationError(msg)
        return value

    class Meta:
        model = Poll
        fields = ('choice',)
