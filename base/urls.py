from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

from .routers import router

schema_view = get_swagger_view(title='Polls API v1')
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include(router.urls)),
    path(
        'api/v1/auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'api/v1/docs/', schema_view)]
