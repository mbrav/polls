from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .models import AnonUser, Answer, Choice, Poll, Vote
from .permissions import IsAuthenticated, IsAuthorOrReadOnlyPermission
from .serializers import (AnonTokenSerializer, AnswerSerializer,
                          PollAddChoiceSerializer, PollCloseSerializer,
                          PollExtendSerializer, PollSerializer, VoteSerializer)
from .utils import Util


def _get_user(request):
    """Get user instance"""
    return request.user


class AnonUserGenToken(ObtainAuthToken):
    """Custom token generation based on user IP"""

    serializer_class = AnonTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        ip = serializer.validated_data['ip_address']

        if not user:
            user = AnonUser(ip_address=ip)
            user.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'ip': user.ip_address,
            'username': user.username,
        })


class PollViewSet(viewsets.ModelViewSet):
    """Poll View Class"""

    queryset = Poll.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_serializer_class(self):
        """Custom serializer classes for different methods"""

        if self.action == 'extend':
            return PollExtendSerializer
        if self.action == 'close':
            return PollCloseSerializer
        if self.action == 'add_choice':
            return PollAddChoiceSerializer
        return PollSerializer

    def perform_create(self, serializer):
        """Create New Poll"""

        user = _get_user(self.request)
        serializer.save(owner=user)

    @action(detail=False, methods=['get'])
    def my(self, request, pk=None):
        """List polls created by user"""

        user = _get_user(request)
        queryset = Poll.objects.filter(owner=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def are_open(self, request, pk=None):
        """List polls that are open"""

        today = Util.time_now()
        queryset = Poll.objects.filter(
            date_end__date__gt=today)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close poll by setting poll's end date to current date
        if close_date is not provided, otherwise set to provided close_date"""

        user = _get_user(request)

        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        time = request.data.get('date_end', None)
        if time:
            serializer.save(owner=user, date_end=time)
        else:
            now = Util.time_now()
            serializer.save(owner=user, date_end=now)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['post'])
    def extend(self, request, pk=None):
        """Open poll by extending poll's end date by 1 day from now"""

        user = _get_user(request)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = request.data.dict()
        time = data.pop('date_end', None)
        if time:
            serializer.save(owner=user, date_end=time)
        else:
            date_end = Util.close_date(instance.date_end, **data)
            serializer.save(owner=user, date_end=date_end)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['post'])
    def add_choice(self, request, pk=None):
        """Add choice to poll"""

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        choice_text = serializer.validated_data.get('choice')
        new_choice = Choice(poll=instance, text=choice_text)
        new_choice.save()

        return Response(serializer.validated_data,
                        status=status.HTTP_201_CREATED)


class VoteViewSet(viewsets.ModelViewSet):
    """Vote View Class"""

    serializer_class = VoteSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnlyPermission)
    queryset = Vote.objects.all()

    def list(self, request, *args, **kwargs):
        """Get list of votes made by user"""

        user = _get_user(self.request)
        queryset = Vote.objects.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """Make a vote"""
        user = _get_user(self.request)
        serializer.save(user=user)


class AnswerViewSet(viewsets.ModelViewSet):
    """Answer View Class"""

    serializer_class = AnswerSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnlyPermission)
    queryset = Answer.objects.all()

    def list(self, request, *args, **kwargs):
        """Get list of answers made by user"""

        user = _get_user(self.request)
        queryset = Answer.objects.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """Make an answer"""
        user = _get_user(self.request)
        serializer.save(user=user)
