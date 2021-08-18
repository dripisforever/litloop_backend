# from __future__ import absolute_import
from django.urls import path
from artists.views import (
    SearchArtistAPIView,
    ArtistDetailAPIView,
    ArtistAlbumsAPIView,
    ArtistRelatedArtistsDetailAPIView,
    ArtistListAPIView,
    ArtistAPIView,

    ArtistAlbumsOldAPIView,
    # FeedAPIView,
)

urlpatterns = [
    path('', ArtistListAPIView.as_view(), name="posts"),
    path('search', SearchArtistAPIView.as_view(), name="search"),
    # path('<int:id>', PostDetailAPIView.as_view(), name="post"),

    path('<str:artist_uri>/upd', ArtistDetailAPIView.as_view(), name="artist_detail"),
    path('<str:artist_uri>/', ArtistAPIView.as_view(), name="artist_detail"),

    path('<str:artist_uri>/albums/upd', ArtistAlbumsAPIView.as_view(), name="artist_detail"),
    path('<str:artist_uri>/albums/', ArtistAlbumsAPIView.as_view(), name="artist_detail"),
    path('<str:artist_uri>/albums/old', ArtistAlbumsOldAPIView.as_view(), name="artist_detail"),

    path('<str:artist_uri>/related_artists/', ArtistRelatedArtistsDetailAPIView.as_view(), name="artist_detail"),
    path('<str:artist_uri>/related_artists/upd', ArtistRelatedArtistsDetailAPIView.as_view(), name="artist_detail"),
]
