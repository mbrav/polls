from rest_framework import serializers

from .models import Choice, Poll, Vote


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
        percent = obj.vote.count() / total_vote_count * 100
        return percent

    class Meta:
        model = Choice
        fields = ('id', 'text', 'count', 'count_percent')


class VoteSerializer(serializers.ModelSerializer):
    """
    Base Vote serializer
    """

    poll = serializers.SlugRelatedField(
        queryset=Poll.objects.all(),
        slug_field='name',
    )

    choice = serializers.SlugRelatedField(
        queryset=Choice.objects.all(),
        slug_field='text',
    )

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
