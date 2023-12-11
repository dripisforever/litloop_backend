# from __future__ import absolute_import
from django.urls import path
from movies.views import (
    ViewsUP,
    AddMovie,
    FeedMovies
)



urlpatterns = [

    path('up', ViewsUP.as_view()),

    path('add', AddMovie.as_view()),

    path('feed/', FeedMovies.as_view()),


]
