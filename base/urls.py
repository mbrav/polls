from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from polls.views import AnonUserGenToken

from .routers import router

schema_view = get_schema_view(
    openapi.Info(
        title='Polls API Docs',
        default_version='v1',
        description='Polls API Schema',
        terms_of_service='https://github.com/mbrav/polls',
        contact=openapi.Contact(email='mbrav@protonmail.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/token/',
         AnonUserGenToken.as_view(),
         name='token_get'),
    path('api/v1/', include(router.urls)),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(
            cache_timeout=0),
        name='schema-json'),
    path(
        'swagger/', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    path(
        '', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]
