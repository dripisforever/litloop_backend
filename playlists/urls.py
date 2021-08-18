# from __future__ import absolute_import
from django.urls import path
from playlists.views import (
    # PlaylistAPIView,
    PlaylistDetailAPIView,
    PlaylistOffsetAPIView,
    # PlaylistDetailedAPIView,
)

from likes.api.views import (
    LikeListAPIView,
    PostLikedByList,
    LikedCountAPIView,
    LikeToggleView,
    LikedIDsAPIView,
)

urlpatterns = [
    # path('', AlbumListAPIView.as_view(), name="posts"),
    # path('feed/', FeedAPIView.as_view(), name="feed"),

    # path('<str:playlist_uri>/like/', LikeToggleView.as_view(), name="post"),
    # path('<int:id>/fike/', AlbumLikeAPIView.as_view(), name="post"),
    # path('<str:playlist_uri>/fike/', TestAlbumLikeAPIView.as_view(), name="post"),

    # path('<int:id>/likers/', PostLikedByList.as_view(), name="post"),
    # path('<int:id>/', PlaylistAPIView.as_view(), name="album_detail"),
    # path('<int:id>/upd', PlaylistAPIView.as_view(), name="album_detail"),
    path('<str:playlist_uri>/', PlaylistDetailAPIView.as_view(), name="album_detail"),
    path('<str:playlist_uri>/tracks', PlaylistOffsetAPIView.as_view(), name="album_detail"),
    # path('<str:playlist_uri>/upd', PlaylistDetailedAPIView.as_view(), name="album_detail"),


]
