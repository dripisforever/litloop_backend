from django.apps import apps
from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

# import tracks.models as Track

# from artists.models import Artist
# from albums.models import Album
# from .models import Track

from likes import services as likes_services


Track = apps.get_model(app_label='tracks', model_name='Track')
Artist = apps.get_model(app_label='artists', model_name='Artist')
Album = apps.get_model(app_label='albums', model_name='Album')
Like = apps.get_model(app_label='likes', model_name='Like')
Image = apps.get_model(app_label='images', model_name='Image')


class ArtistsSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    class Meta:
        model = Artist
        fields = [
            'id',
            'name',
            'artist_uri',

        ]

    def get_id(self, obj):

        return obj.artist_uri


class TracksSerializer(serializers.ModelSerializer):

    artists = ArtistsSerializer(many=True)
    is_liked = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = [
            'id',
            'pk',
            'name',
            'track_uri',
            'is_liked',
            'total_likes',
            'artists',
            'track_number',

        ]

    def get_id(self, obj):

        return obj.track_uri

    def get_is_liked(self, obj):

        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)

    def get_total_likes(self, obj):
        return likes_services.get_object_likes_count(obj)


class ImagesSerializer(serializers.ModelSerializer):

    # artists = ArtistsSerializer(many=True)

    class Meta:
        model = Image
        fields = [
            'id',
            'url',
            'height',
            'width',

        ]


class AlbumSerializer(serializers.ModelSerializer):

    artists = ArtistsSerializer(many=True)
    tracks = TracksSerializer(many=True)
    images = ImagesSerializer(many=True)
    id = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = [
            'id',
            'name',
            'album_uri',
            'artists',
            'tracks',
            'images',
        ]

    def get_id(self, obj):

        return obj.album_uri

class TrackSerializer(serializers.ModelSerializer):
    artists = ArtistsSerializer(many=True)
    album = AlbumSerializer()
    is_liked = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = [
            'id',
            'pk',
            # 'uuid',
            'name',
            'track_uri',
            'track_number',
            'is_liked',
            'total_likes',
            'artists',
            'album',

            # 'created_at',
            # 'updated_at',
        ]

    def get_id(self, obj):

        return obj.track_uri

    def get_is_liked(self, obj):

        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)

    def get_total_likes(self, obj):
        return likes_services.get_object_likes_count(obj)


class AlbumSerializer(serializers.ModelSerializer):

    artists = ArtistsSerializer(many=True)
    # tracks = TracksSerializer(many=True)
    images = ImagesSerializer(many=True)
    id = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = [
            'id',
            'name',
            'album_uri',
            'artists',
            # 'tracks',
            'images',
        ]

    def get_id(self, obj):

        return obj.album_uri


class TrackListSerializer(serializers.ModelSerializer):
    artists = ArtistsSerializer(many=True)
    album = AlbumSerializer()
    is_liked = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = [
            'id',
            # 'pk',
            # 'uuid',
            'name',
            'track_uri',
            'track_number',
            'is_liked',
            'total_likes',
            'artists',
            'album',

            # 'created_at',
            # 'updated_at',
        ]

    def get_id(self, obj):

        return obj.track_uri

    def get_is_liked(self, obj):

        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)

    def get_total_likes(self, obj):
        return likes_services.get_object_likes_count(obj)
