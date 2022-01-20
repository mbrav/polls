from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .models import Choice, Poll, Vote
from .serializers import ChoiceSerializer, PollSerializer, VoteSerializer
from .utils import Util


def _get_user(request):
    """Get user instance"""
    user = get_object_or_404(User, id=request.user.id)
    return user


class PollViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """Poll View Class"""

    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    pagination_class = LimitOffsetPagination

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
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close poll by setting poll's end date to current date"""

        # user = _get_user(request)
        poll = get_object_or_404(queryset, pk=pk)

        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def extend(self, request, pk=None):
        """Open poll by extending poll's end date by 1 day"""

        user = _get_user(request)
        queryset = Poll.objects.filter(owner=user)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class VoteViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """Vote View Class"""

    serializer_class = VoteSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = _get_user(self.request)
        queryset = Vote.objects.filter(user=user)
        return queryset

    def list(self, request, *args, **kwargs):
        """Get list of votes made by user"""

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Make a vote"""
        user = _get_user(self.request)
        serializer.save(user=user)
