from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Choice, Poll
from .serializers import ChoiceSerializer, PollSerializer


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    @action(detail=True, methods=['post', 'get'])
    def vote(self, request, pk=None):
        poll = get_object_or_404(Poll, pk=pk)

        if request.method == 'GET':
            choices = Choice.objects.filter(poll=poll)
            serializer = ChoiceSerializer(choices)
            return Response(serializer.data)
