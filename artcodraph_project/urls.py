"""artcodraph_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static
from .views import start_stream, stop_stream
# from authentication import views as users_views
# from users import views as users_views
# from posts import views as posts_views
# from likes import views as likes_views

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def fake_view(*args, **kwargs):
    """ This view should never be called because the URL paths
        that map here will be served by nginx directly.
    """
    raise Exception("This should never be called!")

urlpatterns = [
    path('admin/', admin.site.urls),

    path("start_stream", start_stream, name="start-stream"),
    path("stop_stream", stop_stream, name="stop-stream"),
    path("live/<username>/index.m3u8", fake_view, name="hls-url"),


    path('users/', include('users.urls')),
    path('posts/', include('posts.urls')),
    path('artist/', include('artists.urls')),
    path('album/', include('albums.urls')),
    path('track/', include('tracks.urls')),
    path('playlist/', include('playlists.urls')),
    # path('v1/', include()),

    # Documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
