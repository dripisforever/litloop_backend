# from __future__ import absolute_import
from django.urls import path
from tracks.views import (
    # PostDetailAPIView,
    # PostListAPIView,
    # PostSearchAPIView,
    TrackDetailAPIView,
    TrackGetOrCreateAPIView,
    SearchTrackAPIView,
    TrackListAPIView,
    TrackPaginationAPIView,
)

from likes.api.views import (
    LikeListAPIView,
    PostLikedByList,
    LikedCountAPIView,
    LikeToggleView,
    LikedIDsAPIView
)

urlpatterns = [
    path('', TrackListAPIView.as_view(), name="posts"),
    # path('', TrackPaginationAPIView.as_view(), name="posts"),
    path('search', SearchTrackAPIView.as_view(), name="search"),
    # path('<int:id>', PostDetailAPIView.as_view(), name="post"),

    path('<int:id>/like/', LikeToggleView.as_view(), name="post"),
    path('<int:id>/likers/', PostLikedByList.as_view(), name="post"),
    path('<str:track_uri>/upd', TrackGetOrCreateAPIView.as_view(), name="track_detail"),
    path('<str:track_uri>/', TrackDetailAPIView.as_view(), name="track_detail"),

]
