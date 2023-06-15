# from __future__ import absolute_import
from django.urls import path
from albums.views import (
    SearchAlbumAPIView,
    AlbumDetailAPIView,
    AlbumDetailedAPIView,
    AlbumListAPIView,
    AlbumPaginationAPIView,
    AlbumAPIView,

    AlbumLikeAPIView,
    TestAlbumLikeAPIView,
    FeedAPIView,
)

from likes.api.views import (
    LikeListAPIView,
    PostLikedByList,
    LikedCountAPIView,
    LikeToggleView,
    LikedIDsAPIView,
)
from views.views import ViewView

urlpatterns = [
    # path('<int:id>', PostDetailAPIView.as_view(), name="post"),
    path('', AlbumListAPIView.as_view(), name="posts"),
    # path('', AlbumPaginationAPIView.as_view(), name="posts"),
    path('search', SearchAlbumAPIView.as_view(), name="search"),
    path('feed/', FeedAPIView.as_view(), name="feed"),

    # path('<int:id>/like/', LikeToggleView.as_view(), name="post"),
    path('<str:album_uri>/like/', LikeToggleView.as_view(), name="post"),
    # path('<int:id>/fike/', AlbumLikeAPIView.as_view(), name="post"),
    path('<str:album_uri>/fike/', TestAlbumLikeAPIView.as_view(), name="post"),

    path('<int:id>/likers/', PostLikedByList.as_view(), name="post"),
    path('<int:id>/upd', AlbumAPIView.as_view(), name="album_detail"),
    path('<str:album_uri>/upd', AlbumDetailAPIView.as_view(), name="album_detail_upd"),
    path('<str:album_uri>/', AlbumDetailedAPIView.as_view(), name="album_detail"),

    path('<int:pk>/view/', ViewView.as_view(), name='view'),

]
