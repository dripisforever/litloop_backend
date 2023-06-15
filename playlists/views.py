from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType
from drf_yasg import openapi as openapi
from drf_yasg.utils import swagger_auto_schema

import requests

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
from rest_framework.parsers import (
    FileUploadParser,
    FormParser,
    JSONParser,
    MultiPartParser,
)
from .serializers import (

    PlaylistDetailSerializer,
    PlaylistSerializer,

)
from posts.renderers import PostRenderer, FeedRenderer, AlbumFeedRenderer, PaginationOffsetRenderer

# from .models import Playlist
# from .serializers import AlbumsSerializer
# from .serializers import AlbumSerializer
# from tracks.pagination import CustomPagination
# from albums.pagination import CustomPagination
from tracks.models import Track
from tracks.serializers import TrackSerializer
import json
# Create your views here.

# from litloop_project.permissions import IsAuthorizedToAdd, IsUserOrEditor, user_allowed_to_upload


# class PlaylistAPIView(RetrieveAPIView):
#     queryset = Playlist.objects.all()
#     serializer_class = PlaylistsSerializer
#     lookup_field = 'id'


class PlaylistDetailAPIView(RetrieveAPIView):
    # serializer_class = PostSerializer
    # permission_classes = (IsAuthenticated, )
    # serializer_class = AlbumsSerializer
    # queryset = Playlist.objects.all()
    lookup_field = 'playlist_uri'

    # def get_queryset(self):
    #     return self.queryset.filter(author=self.request.user)

    def get(self, request, playlist_uri):
        # SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        # SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        SPOTIPY_CLIENT_ID = "0575ef8642c94277b3fec71f400ee600"
        SPOTIPY_CLIENT_SECRET = "21c16d49607b49cd8bbe4a5897c63de4"


        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )


        spotify_url = 'https://api.spotify.com/v1/playlists/'
        results = sp.playlist(playlist_uri)
        dataset = []
        return Response(results)



class PlaylistOffsetAPIView(RetrieveAPIView):

    lookup_field = 'playlist_uri'
    renderer_classes = (PaginationOffsetRenderer,)

    # http://localhost:8000/playlist/4mloXTyQUOSnCLJTeBSfnR/tracks?offset=100&limit=100
    def get(self, request, playlist_uri):
        # SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        # SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        SPOTIPY_CLIENT_ID = "0575ef8642c94277b3fec71f400ee600"
        SPOTIPY_CLIENT_SECRET = "21c16d49607b49cd8bbe4a5897c63de4"

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )

        offset = request.GET.get('offset')
        limit = request.GET.get('limit')
        results = sp.playlist_tracks(playlist_uri, offset=offset, limit='100')
        # results = sp.playlist_tracks(playlist_uri, offset, limit)


        return Response(results)


class PlaylistList(APIView):
    """Playlists listings and creation views"""

    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorizedToAdd)
    parser_classes = (JSONParser, MultiPartParser, FormParser, FileUploadParser)

    @swagger_auto_schema(
        manual_parameters=[],
        tags=['Playlists'],
        operation_summary='to_be_written',
        operation_description='to_be_written',
        responses={
            200: openapi.Response('response description', PlaylistSerializer(many=True)),
        },
    )
    def get(self, request, format=None):
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        playlists = Playlist.objects.filter().prefetch_related("user")

        if "author" in self.request.query_params:
            author = self.request.query_params["author"].strip()
            playlists = playlists.filter(user__username=author)

        page = paginator.paginate_queryset(playlists, request)

        serializer = PlaylistSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(manual_parameters=[], tags=['Playlists'], operation_summary='to_be_written', operation_description='to_be_written',)
    def post(self, request, format=None):
        serializer = PlaylistSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PlaylistDetail(APIView):
#     """Playlist related views"""
#
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUserOrEditor)
#     parser_classes = (JSONParser, MultiPartParser, FormParser, FileUploadParser)
#
#     def get_playlist(self, friendly_token):
#         try:
#             playlist = Playlist.objects.get(friendly_token=friendly_token)
#             self.check_object_permissions(self.request, playlist)
#             return playlist
#         except PermissionDenied:
#             return Response({"detail": "not enough permissions"}, status=status.HTTP_400_BAD_REQUEST)
#         except BaseException:
#             return Response(
#                 {"detail": "Playlist does not exist"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#     @swagger_auto_schema(manual_parameters=[], tags=['Playlists'], operation_summary='to_be_written', operation_description='to_be_written',)
#     def get(self, request, friendly_token, format=None):
#         playlist = self.get_playlist(friendly_token)
#         if isinstance(playlist, Response):
#             return playlist
#
#         serializer = PlaylistDetailSerializer(playlist, context={"request": request})
#
#         playlist_media = PlaylistMedia.objects.filter(playlist=playlist).prefetch_related("media__user")
#
#         playlist_media = [c.media for c in playlist_media]
#         playlist_media_serializer = MediaSerializer(playlist_media, many=True, context={"request": request})
#         ret = serializer.data
#         ret["playlist_media"] = playlist_media_serializer.data
#
#         return Response(ret)
#
#     @swagger_auto_schema(manual_parameters=[], tags=['Playlists'], operation_summary='to_be_written', operation_description='to_be_written',)
#     def post(self, request, friendly_token, format=None):
#         playlist = self.get_playlist(friendly_token)
#         if isinstance(playlist, Response):
#             return playlist
#         serializer = PlaylistDetailSerializer(playlist, data=request.data, context={"request": request})
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @swagger_auto_schema(manual_parameters=[], tags=['Playlists'], operation_summary='to_be_written', operation_description='to_be_written',)
#     def put(self, request, friendly_token, format=None):
#         playlist = self.get_playlist(friendly_token)
#         if isinstance(playlist, Response):
#             return playlist
#         action = request.data.get("type")
#         media_friendly_token = request.data.get("media_friendly_token")
#         ordering = 0
#         if request.data.get("ordering"):
#             try:
#                 ordering = int(request.data.get("ordering"))
#             except ValueError:
#                 pass
#
#         if action in ["add", "remove", "ordering"]:
#             media = Media.objects.filter(friendly_token=media_friendly_token).first()
#             if media:
#                 if action == "add":
#                     media_in_playlist = PlaylistMedia.objects.filter(playlist=playlist).count()
#                     if media_in_playlist >= settings.MAX_MEDIA_PER_PLAYLIST:
#                         return Response(
#                             {"detail": "max number of media for a Playlist reached"},
#                             status=status.HTTP_400_BAD_REQUEST,
#                         )
#                     else:
#                         obj, created = PlaylistMedia.objects.get_or_create(
#                             playlist=playlist,
#                             media=media,
#                             ordering=media_in_playlist + 1,
#                         )
#                         obj.save()
#                         return Response(
#                             {"detail": "media added to Playlist"},
#                             status=status.HTTP_201_CREATED,
#                         )
#                 elif action == "remove":
#                     PlaylistMedia.objects.filter(playlist=playlist, media=media).delete()
#                     return Response(
#                         {"detail": "media removed from Playlist"},
#                         status=status.HTTP_201_CREATED,
#                     )
#                 elif action == "ordering":
#                     if ordering:
#                         playlist.set_ordering(media, ordering)
#                         return Response(
#                             {"detail": "new ordering set"},
#                             status=status.HTTP_201_CREATED,
#                         )
#             else:
#                 return Response({"detail": "media is not valid"}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(
#             {"detail": "invalid or not specified action"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#
#     @swagger_auto_schema( manual_parameters=[], tags=['Playlists'], operation_summary='to_be_written', operation_description='to_be_written',)
#     def delete(self, request, friendly_token, format=None):
#         playlist = self.get_playlist(friendly_token)
#         if isinstance(playlist, Response):
#             return playlist
#
#         playlist.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# Dark Codeine
# http://localhost:8000/playlist/1iC9VT69XLLRPtrkBA7tCT/?format=json
# https://open.spotify.com/playlist/1iC9VT69XLLRPtrkBA7tCT
# 37i9dQZEVXbLnolsZ8PSNw
# http://localhost:8000/playlist/4mloXTyQUOSnCLJTeBSfnR/?format=json
#

# Nelly Furtado
# https://open.spotify.com/playlist/2icgLCTGOep0uvt6ofEdCM?si=3e9344ca3cda4fdf
