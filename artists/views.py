from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import pprint

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
from rest_framework.renderers import JSONRenderer

from rest_framework.permissions import IsAuthenticated
from posts.renderers import PostRenderer
from .models import Artist
from .serializers import ArtistSerializer, ArtistListSerializer



class ArtistListAPIView(ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistListSerializer


class SearchArtistAPIView(APIView):
    # lookup_field = 'track_uri'
    renderer_classes = (PostRenderer,)
    # serializer_class = PostSerializer
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

        search_result = sp.search(term, limit=10, type='artist')
        # res = PostSerializer(search_result)
        # return Response(search_result)
        # return Response(res)
        return Response(search_result.get('artists'))


class ArtistDetailAPIView(RetrieveAPIView):
    # serializer_class = PostSerializer
    renderer_classes = [JSONRenderer]
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
        # from artists.models import Artist
        from albums.models import Album
        # from images.models import Image

        artist_info = sp.artist(artist_uri)
        # musicbot = Music.create(artist)
        artist_albums_info = sp.artist_albums(artist_uri, limit=10)
        # artist_related_artists_info = sp.artist_related_artists(artist_uri)

        artist = Artist.create(**artist_info)

        for album_data in artist_albums_info['items']:
            album_uri = album_data['id']
            album_info = sp.album(album_uri)
            album = Album.create(**album_info)

        # for album_data in artist_related_artists_info['items']:
        #     album_uri = album_data['id']
        #     album_info = sp.album(album_uri)
        #     album = Album.create(**album_info)

        snippet = Artist.objects.get(artist_uri=artist_uri)
        serializer = ArtistSerializer(snippet, context={'request': self.request})
        return Response(serializer.data)

        # return Response(artist_info)


class ArtistAPIView(RetrieveAPIView):
    # serializer_class = PostSerializer
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
        # from artists.models import Artist
        from albums.models import Album
        # from images.models import Image

        artist_info = sp.artist(artist_uri)

        return Response(artist_info)


class ArtistAlbumsAPIView(RetrieveAPIView):
    renderer_classes = (PostRenderer,)
    # serializer_class = PostSerializer
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
        from albums.models import Album
        artist_albums_info = sp.artist_albums(artist_uri, limit=10)

        # album_uri = track_data['album']['id']
        # album_data = sp.album(album_uri)
        # album = Album.create(**album_data)

        # track = Track.create(**track_data)

        for album_data in artist_albums_info['items']:
            album_uri = album_data['id']
            album_data = sp.album(album_uri)
            Album.create(**album_data)
        #
        #
        #
        #
        # snippet = Track.objects.get(track_uri=track_uri)
        # serializer = TrackSerializer(snippet, context={'request': self.request})
        # return Response(serializer.data)

        snippet = Artist.objects.get(artist_uri=artist_uri)
        serializer = ArtistSerializer(snippet, context={'request': self.request})
        return Response(serializer.data)

class ArtistAlbumsOldAPIView(RetrieveAPIView):
    renderer_classes = (PostRenderer,)
    # serializer_class = PostSerializer
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
        from albums.models import Album
        artist_albums_info = sp.artist_albums(artist_uri, limit=10)

        # album_uri = track_data['album']['id']
        # album_data = sp.album(album_uri)
        # album = Album.create(**album_data)

        # track = Track.create(**track_data)

        # for album_data in artist_albums_info['items']:
        #     album_uri = album_data['id']
        #     album_data = sp.album(album_uri)
        #     Album.create(**album_data)
        # #
        # #
        # #
        # #
        # # snippet = Track.objects.get(track_uri=track_uri)
        # # serializer = TrackSerializer(snippet, context={'request': self.request})
        # # return Response(serializer.data)
        #
        # snippet = Artist.objects.get(artist_uri=artist_uri)
        # serializer = ArtistSerializer(snippet, context={'request': self.request})
        # return Response(serializer.data)

        return Response(artist_albums_info)


class ArtistRelatedArtistsDetailAPIView(RetrieveAPIView):
    # serializer_class = PostSerializer
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
