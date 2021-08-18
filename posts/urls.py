# from __future__ import absolute_import
from django.urls import path
from .views import (
    PostDetailAPIView,
    PostListAPIView,
    # PostLikeAPIView,
    # PostSearchAPIView,
    TrackDetailAPIView,
    SearchTrackAPIView,
    SearchAlbumAPIView,
    SearchArtistAPIView,
    ArtistDetailAPIView,
    AlbumDetailAPIView,
    ArtistAlbumsDetailAPIView,
    ArtistRelatedArtistsDetailAPIView,
    FeedAPIView,
    PostCreateAPIView,
    NewReleasesAPIView,
)

from likes.api.views import (
    LikeListAPIView,
    PostLikedByList,
    LikedCountAPIView,
    LikeToggleView,
    LikedIDsAPIView
)

urlpatterns = [
    # path('feed/',                   view=views.Images.as_view(), name='feed'),
    # path('post/:id/likes/$',        view=views.LikeImage.as_view(), name='like_image'),
    # path('post/:id/unlikes/$',      view=views.UnLikeImage.as_view(), name='like_image'),
    # path('post/:id/comments/$',     view=views.CommentOnImage.as_view(), name='comment_image'),
    # path('post/:id/comments/:id/$', view=views.ModerateComments.as_view(), name='comment_image'),
    # path('comments/:id/$',          view=views.Comment.as_view(), name='comment'),
    path('', PostListAPIView.as_view(), name="posts"),
    path('create/', PostCreateAPIView.as_view(), name="posts"),
    path('feed/', FeedAPIView.as_view(), name="feed"),
    path('feed/upd/', NewReleasesAPIView.as_view(), name="feed"),
    path('<int:id>/', PostDetailAPIView.as_view(), name="post"),
    path('<int:id>/like/', LikeToggleView.as_view(), name="post"),
    path('<int:id>/likers/', PostLikedByList.as_view(), name="post"),

    path('search/artist', SearchArtistAPIView.as_view(), name="search"),
    path('search/album', SearchAlbumAPIView.as_view(), name="search"),
    path('search/track', SearchTrackAPIView.as_view(), name="search"),
    # path('search', SearchAlbumAPIView.as_view(), name="search"),

    # path('search', PostSearchAPIView.as_view(), name="search"),
]
