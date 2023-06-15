from django.apps import apps
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

# from albums.models import Album
# from artists.models import Artist
# from likes.models import Like

# import artists.models as Artist
# import albums.models as Album
# import likes.models as Like

# Track = apps.get_model(app_label='tracks', model_name='Track')
# Artist = apps.get_model(app_label='artists', model_name='Artist')
# Album = apps.get_model(app_label='albums', model_name='Album')
# Like = apps.get_model(app_label='likes', model_name='Like')

# from media.media_choice import MEDIA_STATES, MEDIA_TYPES, MEDIA_ENCODING_STATUS, ENCODE_EXTENSIONS, ENCODE_RESOLUTIONS, CODECS
#
#
# class UserUploadedTrack(models.Model):
#     name = models.CharField()
#     artist_name = models.CharField()
#     user = models.ForeignKey('users.User', related_name='tracks')
#     state = models.CharField(max_length=20, choices=MEDIA_STATES, default=helpers.get_portal_workflow(), db_index=True)

class Track(models.Model):
    track_uri = models.CharField(max_length=400)
    name = models.CharField(max_length=400)
    track_number = models.CharField(max_length=400, default="")
    artists = models.ManyToManyField('artists.Artist', related_name='tracks')
    album = models.ForeignKey('albums.Album', related_name='tracks', on_delete=models.CASCADE)
    likes = GenericRelation('likes.Like', related_query_name='track_likes', null=True)
    # tags = GenericRelation('likes.Tag', related_query_name='track_tags', null=True)
    # comments = GenericRelation('comments.Comment', related_query_name='track_comments', null=True)

    # # author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    # deezer_id = models.CharField(max_length=MAX_LENGTH, null=True, unique=True)
    # spotify_id = models.CharField(max_length=MAX_LENGTH, null=True, unique=True)
    # apple_music_id = models.CharField(max_length=MAX_LENGTH, null=True, unique=True)
    # isrc = models.CharField(max_length=MAX_LENGTH, null=True)

    @classmethod
    def create(cls, **kwargs):
        from artists.models import Artist
        from albums.models import Album
        from images.models import Image

        album, created = Album.objects.get_or_create(
            album_uri = kwargs['album']['id'],
            name = kwargs['album']['name']

        )

        for album_artists in kwargs['album']['artists']:
            artist, created = Artist.objects.get_or_create(
                artist_uri = album_artists["id"],
                name = album_artists["name"]

            )
            album.artists.add(artist)

        track, created = cls.objects.get_or_create(
            track_uri = kwargs['id'],
            name = kwargs['name'],
            album_id = album.id,
            track_number = kwargs['track_number'],
        )
        # track.album.add(album)
        for artists_data in kwargs['artists']:

            artist, created = Artist.objects.get_or_create(
                artist_uri = artists_data["id"],
                name = artists_data["name"]

            )
            track.artists.add(artist)


        return track

    @property
    def total_likes(self):
        return self.likes.count()

    def likes_count(self):
        return self.likes.count()

# json_data = json.loads(data_file.read())
#
#     for track_data in json_data:
#         track = Track.create(**track_data)
