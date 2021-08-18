from rest_framework import serializers
from .models import Album
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
# import tracks.models as Track
from tracks.models import Track
# from artists.models import Artist

from django.apps import apps

# Track = apps.get_model('tracks', 'Track')
Artist = apps.get_model('artists', 'Artist')

class ArtistsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = [
            'id',
            'name',
        ]


class TrackSerializer(serializers.ModelSerializer):
    artists = ArtistsSerializer(many=True)

    class Meta:
        model = Track
        fields = [
            'id',
            'name',
            'artists',
        ]


class AlbumsSerializer(serializers.ModelSerializer):
    artists = ArtistsSerializer(many=True)
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = [
            'id',
            'name',
            'artists',
            'tracks',
        ]
