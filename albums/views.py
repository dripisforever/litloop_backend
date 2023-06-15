from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import pprint

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView,
    GenericAPIView,
)
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from posts.renderers import PostRenderer, FeedRenderer, AlbumFeedRenderer
from .models import Album
from .serializers import AlbumsSerializer
# from .serializers import AlbumSerializer
# from tracks.pagination import CustomPagination
from albums.pagination import CustomPagination
from tracks.models import Track
from tracks.serializers import TrackSerializer
import json



    # permission_classes = (permissions.IsAuthenticated,)
class PagePagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 3

    default_limit = 2
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 50

class AlbumListAPIView(ListAPIView):
    queryset = Album.objects.all()
    pagination_class = PagePagination
    serializer_class = AlbumsSerializer

# class FeedAPIView(ListCreateAPIView, LimitOffsetPagination):
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10

class FeedAPIView(APIView, PageNumberPagination):
    # renderer_classes = (AlbumFeedRenderer,)

    serializer_class = AlbumsSerializer
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'
    # pagination_class = PagePagination

    # permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def get(self, request, *args, **kwargs):
        SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )
        feed_info = sp.new_releases(country="US", limit='50', )

        # return Response(feed_info.get('albums'))

        for album_data in feed_info['albums']['items']:
            album_uri = album_data['id']
            album_info = sp.album(album_uri)
            album = Album.create(**album_info)
            # album = await Album.create(**album_info)
            # spotify_task.delay(**album_info)

        queryset = Album.objects.all()
        page = self.paginate_queryset(self, queryset, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(self, serializer.data)
        # snippet = Album.objects.get(album_uri=album_uri)
        snippet = Album.objects.all().order_by('-created_at')
        # serializer = AlbumsSerializer(snippet, context={'request': self.request}, many=True)
        serializer = self.get_serializer(queryset, context={'request': self.request}, many=True)
        # return Response(serializer.data)
        # return Response(serializer.data)
        # return self.get_paginated_response(serializer.data)
        return Response(feed_info)

class AlbumAPIView(RetrieveAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumsSerializer
    lookup_field = 'id'


class AlbumLikeAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Album.objects.all()
    serializer_class = AlbumsSerializer
    lookup_field = 'id'

    def put(self, request, id):
        from likes.models import Like

        user=self.request.user
        content_type=ContentType.objects.get_for_model(Album)
        al = Album.objects.get(id=id)
        like, created = Like.objects.get_or_create(
            content_type=content_type,
            object_id=al.id,
            user=user
        )
        if not created:
            like.delete()

        serializer = AlbumsSerializer(al, context={'request': self.request})
        return Response(serializer.data)

    def delete(self, request, id, format=None):
        snippet = self.get_object(id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TestAlbumLikeAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Album.objects.all()
    serializer_class = AlbumsSerializer
    lookup_field = 'album_uri'

    def put(self, request, album_uri):
        from likes.models import Like

        user=self.request.user
        content_type=ContentType.objects.get_for_model(Album)
        al = Album.objects.get(album_uri=album_uri)
        like, created = Like.objects.get_or_create(
            content_type=content_type,
            object_id=al.id,
            user=user
        )
        if not created:
            like.delete()

        serializer = AlbumsSerializer(al, context={'request': self.request})
        return Response(serializer.data)

    def delete(self, request, album_uri, format=None):
        snippet = self.get_object(album_uri)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchAlbumAPIView(APIView):

    renderer_classes = (PostRenderer,)

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

        search_result = sp.search(term, limit=50, type='album')
        # res = PostSerializer(search_result)
        return Response(search_result.get('albums'))
        # return Response(search_result)
        # return Response(res)


class AlbumDetailAPIView(RetrieveAPIView):
    # serializer_class = PostSerializer
    # permission_classes = (IsAuthenticated, )
    serializer_class = AlbumsSerializer
    queryset = Album.objects.all()
    lookup_field = 'album_uri'

    # def get_queryset(self):
    #     return self.queryset.filter(author=self.request.user)

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

        # payload = {
        #
        #     'tracks': album_info,
        #     'likes_count': '1',
        # }
        # return Response(payload)



        album = Album.create(**album_info)
        # spotify_task.delay(**album_info)

        snippet = Album.objects.get(album_uri=album_uri)
        serializer = AlbumsSerializer(snippet, context={'request': self.request})
        return Response(serializer.data)


class AlbumDetailedAPIView(RetrieveAPIView):
    # serializer_class = PostSerializer
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


class AlbumPaginationAPIView(GenericAPIView):
    # serializer_class = TrackSerializer
    serializer_class = AlbumsSerializer
    queryset = Album.objects.all()
    # queryset = Track.objects.all()
    pagination_class = CustomPagination

    # def get_queryset(self):
    #     return self.queryset.filter(tracks=self.request.user)

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        payload = {
            'return_code': '0000',
            'return_message': 'Success',
            'tracks': data
        }
        return Response(payload)
