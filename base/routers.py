from django.urls import include, path
from rest_framework.routers import DefaultRouter

from polls.views import AnswerViewSet, PollViewSet, VoteViewSet

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='polls')
router.register(r'votes', VoteViewSet, basename='votes')
router.register(r'answers', AnswerViewSet, basename='answers')


urlpatterns = [
    path(r'^', include(router.urls)),
]
