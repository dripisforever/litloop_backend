from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from uploader.channels import TaskProgressConsumer
# from authentication import views as users_views
# from users import views as users_views
# from posts import views as posts_views
# from likes import views as likes_views
# from django.db.models.loading import cache as model_cache
# if not model_cache.loaded:
#     model_cache.get_models()

from uploader.websocket.websocket_views import GetHitmen, StartNewHitJob, ScheduleNewHitJob, CreateUserView

schema_view = get_schema_view(
   openapi.Info(title="LitLoop API", default_version='v1',),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('/', include('media.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('auth.urls')),

    path('fu/', include("uploader.urls", namespace='fineuploader')),
    path('ws/', include("uploader.urls", namespace='websocket')),

    path('users/', include('users.urls')),
    path('videos/', include('videos.urls')),
    # path('media/', include('media.urls')),

    path('posts/', include('posts.urls')),
    path('artist/', include('artists.urls')),
    path('album/', include('albums.urls')),
    path('track/', include('tracks.urls')),
    path('playlist/', include('playlists.urls')),
    path('views/', include('views.urls')),
    # path('v1/', include()),

    # progress bar
    path("hitmen/all", GetHitmen.as_view()),
    path("hitmen/start-job", StartNewHitJob.as_view()),
    path("hitmen/schedule", ScheduleNewHitJob.as_view()),

    # Documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ref docker-celery
websocket_urlpatterns = [
    # path("task/upload/<str:taskID>/", TaskProgressConsumer.as_asgi()),
    # path("task/transcoding/<str:taskID>/", TaskProgressConsumer.as_asgi()),

    path("task/progress/<str:taskID>/", TaskProgressConsumer.as_asgi()),
]
