# -*- coding: utf-8 -*-
# from django.conf.urls import re_path
from django.urls import path
from . import views
from .views import FineUploaderView

# from hitman_rest_api.channels import TaskProgressConsumer
from uploader.channels import TaskProgressConsumer
from uploader.websocket.websocket_views import GetHitmen, StartNewHitJob, ScheduleNewHitJob, CreateUserView

app_name = "uploader"

urlpatterns = [
    # re_path(r"^upload/", views.FineUploaderView.as_view(), name="upload"),

    # re_path(r"^upload/", views.FineUploaderView.as_view(), name="upload"),
    # re_path(r"upload", views.FineUploaderView.as_view(), name="upload"),
    # path(r"upload", views.FineUploaderView.as_view(), name="upload"),

    path('upload/', views.FineUploaderView.as_view(), name="upload"),
    # path('start-upload/', views.FineUploaderView.as_view(), name="upload"),
    # path('complete-upload/', views.FineUploaderView.as_view(), name="upload"),
    # path('get-upload-url/', views.FineUploaderView.as_view(), name="upload"),

    # re_path(r"^upload", FineUploaderView.as_view(), name="upload"),
    # path('upload', FineUploaderView.as_view(), name="upload"),

    # path("hitmen/all", GetHitmen.as_view()),
    # path("hitmen/start-job", StartNewHitJob.as_view()),
    # path("hitmen/schedule", ScheduleNewHitJob.as_view()),

    # path("uploader/all", GetHitmen.as_view()),
    # path("uploader/start-job", StartNewHitJob.as_view()),
    # path("uploader/schedule", ScheduleNewHitJob.as_view()),
]

# ref docker-celery
websocket_urlpatterns = [
    # path("task/upload/<str:taskID>/", TaskProgressConsumer.as_asgi()),
    # path("task/transcoding/<str:taskID>/", TaskProgressConsumer.as_asgi()),
    path("task/progress/<str:taskID>/", TaskProgressConsumer.as_asgi()),

]
