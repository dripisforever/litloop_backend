from django.shortcuts import render
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView
)
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from posts.permissions import IsOwner
from posts.models import Post
from posts.renderers import PostRenderer, FeedRenderer, PaginationOffsetRenderer
from users.models import User
from posts.serializers import PostSerializer, PostCreateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    # serializer_class = PostSerializer
    serializer_class = PostCreateSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    # def post(self, request, *args, **kwargs):
    #     # uv = Post(author=self.request.user)
    #     # serializer = self.serializer_class(uv, data=request.data)
    #     serializer = self.serializer_class(data=request.data)
    #     # serializer = self.serializer_class(context={'request': request}, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = (permissions.IsAuthenticated,)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


# class PostGetOrCreateAPIView(ListAPIView):
#
#     def get(self, request, id):
#         """
#         /track/:id/
#         """
#         # track_id = Track.objects.get(id=id)
#         # track_id = Track.objects.get(id=id)
#         # track_id = Track.objects.get_or_create(id=id)
#         user_liked_posts = Post.objects.filter(likes__user=track_id)
#         serializer = PostSerializer(user_liked_posts, many=True, context={'request': request})
#         # user = self.request.user
#         # return Post.objects.filter(likes__user=user.id)
#         # user_id = User.objects.get(id=id)
#         # return self.queryset.filter(likes__user=self.request.GET.id)
#         return Response(serializer.data, status=status.HTTP_200_OK)

from django.db import IntegrityError
from django.shortcuts import get_object_or_404




import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import pprint


class PagePagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 3



class FeedAPIView(ListCreateAPIView):
    renderer_classes = (FeedRenderer,)

    serializer_class = PostSerializer
    pagination_class = PagePagination
    # queryset = Post.objects.all()
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )
        feed_info = sp.new_releases(limit='50')
        return Response(feed_info.get('albums'))
        # return Response(feed_info)


class NewReleasesAPIView(ListCreateAPIView):
    # renderer_classes = (FeedRenderer,)

    serializer_class = PostSerializer
    # pagination_class = PagePagination
    # queryset = Post.objects.all()
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )
        feed_info = sp.new_releases(limit='50')
        return Response(feed_info.get('albums'))
        # return Response(feed_info)


class TrackDetailAPIView(RetrieveAPIView):
    serializer_class = PostSerializer
    lookup_field = 'track_uri'

    def get(self, request, track_uri):
        SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )
        track_info = sp.track(track_uri)
        # Track.objects.get_or_create(track_info)
        return Response(track_info)


class TrackGetOrCreateAPIView(RetrieveAPIView):
    serializer_class = PostSerializer
    lookup_field = 'track_uri'

    def get(self, request, track_uri):
        SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )
        track_info = sp.track(track_uri)
        # Track.objects.get_or_create(track_info)
        return Response(track_info)


class ArtistDetailAPIView(RetrieveAPIView):
    serializer_class = PostSerializer
    lookup_field = 'artist_uri'

    def get(self, request, artist_uri):
        SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )
        artist_info = sp.artist(artist_uri)
        return Response(artist_info)


class ArtistAlbumsDetailAPIView(RetrieveAPIView):
    renderer_classes = (PostRenderer,)
    serializer_class = PostSerializer
    lookup_field = 'artist_uri'

    def get(self, request, artist_uri):
        SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )
        artist_albums_info = sp.artist_albums(artist_uri, limit=50)
        # artist_albums_info = sp.artist_albums(artist_uri, limit=50, offset=100)
        return Response(artist_albums_info)


class ArtistRelatedArtistsDetailAPIView(RetrieveAPIView):
    serializer_class = PostSerializer
    lookup_field = 'artist_uri'

    def get(self, request, artist_uri):
        SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )
        artist_related_artists_info = sp.artist_related_artists(artist_uri)
        return Response(artist_related_artists_info)


class AlbumDetailAPIView(RetrieveAPIView):
    serializer_class = PostSerializer
    lookup_field = 'album_uri'

    def get(self, request, album_uri):
        SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )
        album_info = sp.album(album_uri)
        return Response(album_info)


class SearchArtistAPIView(APIView):
    # lookup_field = 'track_uri'
    # renderer_classes = (PostRenderer,)
    renderer_classes = (PaginationOffsetRenderer,)
    serializer_class = PostSerializer
    def get(self, request):
        term = self.request.query_params.get('q', None)
        SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )
        offset = request.GET.get('offset')
        # limit = request.GET.get('limit')
        search_result = sp.search(term, offset=offset, limit=50, type='artist')

        # search_result = sp.search(term, limit=10, type='artist')
        # res = PostSerializer(search_result)
        return Response(search_result.get('artists'))
        # return Response(search_result)
        # return Response(res)


class SearchTrackAPIView(APIView):
    # lookup_field = 'track_uri'
    # renderer_classes = (PostRenderer,)
    renderer_classes = (PaginationOffsetRenderer,)

    def get(self, request):
        term = self.request.query_params.get('q', None)
        SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )

        offset = request.GET.get('offset')
        # limit = request.GET.get('limit')
        search_result = sp.search(term, offset=offset, limit=50, type='track', market="US")

        # search_result = sp.search(term, limit=10, type='track', market="US")
        # res = PostSerializer(search_result)
        return Response(search_result.get('tracks'))
        # return Response(search_result)
        # return Response(res)


class SearchAlbumAPIView(APIView):

    # lookup_field = 'track_uri'
    # renderer_classes = (PostRenderer,)
    renderer_classes = (PaginationOffsetRenderer,)

    def get(self, request):
        term = self.request.query_params.get('q', None)
        SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )

        offset = request.GET.get('offset')
        # limit = request.GET.get('limit')
        search_result = sp.search(term, offset=offset, limit=50, type='album')
        # search_result = sp.search(term, limit=50, type='album')
        # res = PostSerializer(search_result)
        return Response(search_result.get('albums'))
        # return Response(search_result)
        # return Response(res)
