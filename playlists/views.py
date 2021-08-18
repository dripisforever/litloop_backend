from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType

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
        SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )

        # offset = request.GET.get('offset')
        # limit = request.GET.get('limit')

        # album_info = sp.playlist(playlist_uri)
        # #
        # results = sp.playlist(playlist_uri)
        # tracks = results['tracks']['items']
        # while results['tracks']['next']:
        #     results = sp.next(results)
        #     tracks.extend(results['tracks']['items'])
        #
        # # return Response(tracks)
        # return tracks
        spotify_url = 'https://api.spotify.com/v1/playlists/'
        # requests.get(spotify_url, params={offset: offset, limit: limit})
        # results = sp.playlist_tracks(playlist_uri)
        results = sp.playlist(playlist_uri)
        dataset = []
        # tracks = results['items']
        # while results['next']:
        #     results = sp.next(results)
        #     tracks.extend(results['items'])
            # dataset.append(results['tracks']['items'])
        # results = sp.next(results)
        # return Response(tracks)
        return Response(results)
        # return tracks
        # return Response(album_info)

    # def get_playlist_tracks(playlist_uri):
    #     results = sp.playlist(playlist_uri)
    #     tracks = results['items']
    #     while results['next']:
    #         results = sp.next(results)
    #         tracks.extend(results['items'])
    #     return tracks

    # def get_tracks(sp, playlist):
    #     results = sp.playlist(playlist["id"], fields="tracks,next")
    #     results["next"] = results["tracks"]["next"]
    #     tracks = results["tracks"]["items"]
    #     while results["next"]:
    #         results = sp.next(results)
    #         tracks += results["items"]
    #     return [track["track"] for track in tracks]

class PlaylistOffsetAPIView(RetrieveAPIView):
    # serializer_class = PostSerializer
    # permission_classes = (IsAuthenticated, )
    # serializer_class = AlbumsSerializer
    # queryset = Playlist.objects.all()

    lookup_field = 'playlist_uri'
    renderer_classes = (PaginationOffsetRenderer,)
    # def get_queryset(self):
    #     return self.queryset.filter(author=self.request.user)

    # http://localhost:8000/playlist/4mloXTyQUOSnCLJTeBSfnR/tracks?offset=100&limit=100
    def get(self, request, playlist_uri):
        SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"
        SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

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

# Dark Codeine
# http://localhost:8000/playlist/1iC9VT69XLLRPtrkBA7tCT/?format=json
# https://open.spotify.com/playlist/1iC9VT69XLLRPtrkBA7tCT
# 37i9dQZEVXbLnolsZ8PSNw
# http://localhost:8000/playlist/4mloXTyQUOSnCLJTeBSfnR/?format=json
#

# Nelly Furtado
# https://open.spotify.com/playlist/2icgLCTGOep0uvt6ofEdCM?si=3e9344ca3cda4fdf
