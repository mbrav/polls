from django.urls import include, path
from polls.views import PollViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='polls')


urlpatterns = [
    path('', include(router.urls)),
]
