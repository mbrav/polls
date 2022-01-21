from django.urls import include, path
from polls.views import PollViewSet, VoteViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='polls')
router.register(r'votes', VoteViewSet, basename='votes')


urlpatterns = [
    path(r'^', include(router.urls)),
]
