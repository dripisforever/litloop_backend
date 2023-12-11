from django.apps import apps
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.sites.shortcuts import get_current_site

from artists.models import Artist
from tracks.models import Track
from images.models import Image

# from likes.models import Like

# import artists.models as Artist
# import tracks.models as Track
# import images.models as Image
# import likes.models  as Like

# Track = apps.get_model(app_label='tracks', model_name='Track')
# Artist = apps.get_model(app_label='artists', model_name='Artist')
# Album = apps.get_model(app_label='albums', model_name='Album')
# Like = apps.get_model(app_label='likes', model_name='Like')


class Album(models.Model):
    id = models.BigAutoField(primary_key=True)
    # id = models.CharField(max_length=400, primary_key=True)
    name = models.CharField(max_length=400)
    album_uri = models.CharField(max_length=400)
    artists = models.ManyToManyField('artists.Artist', related_name='albums')
    # images = models.ManyToManyField(Image, related_name='albums')
    # likes  = models.ManyToManyField('users.User', related_name='liked_albums', blank=True, through=AlbumLike)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # faves = ManyToManyField('users.User', related_name='faved_albums', blank=True, through=TweetLike)
    # tracks = ManyToManyField(Track,  through='AlbumTracks')
    # album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    # author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    @classmethod
    def create(cls, **kwargs):

        # from artists.models import Artist
        # from tracks.models import Track
        # from images.models import Image

        # current_site = get_current_site(request).domain

        album, created = cls.objects.get_or_create(
            album_uri = kwargs['id'],
            name = kwargs['name'],
        )

        for artist_data in kwargs['artists']:

            artist, created = Artist.objects.get_or_create(
                artist_uri = artist_data['id'],
                name = artist_data['name'],
            )
            album.artists.add(artist)

        for track_data in kwargs['tracks']['items']:

            track, created = Track.objects.get_or_create(
                track_uri = track_data["id"],
                name = track_data["name"],
                album_id = album.id,
                track_number = track_data['track_number'],
                # href = current_site + "track/" + kwargs['items']['id'] + "/",
            )
            album.tracks.add(track)

            for artist_data in track_data['artists']:
                artist, created = Artist.objects.get_or_create(
                    artist_uri = artist_data['id'],
                    name = artist_data['name'],
                )
                track.artists.add(artist)


        for images_data in kwargs['images']:
            # extract_id_from_url = images_data["url"]
            image, created = Image.objects.get_or_create(
                url = images_data["url"],
                height = images_data["height"],
                width = images_data["width"],
                album_id = album.id,

            )


        # album = cls.objects.update_or_create(
        #     id=1,
        #     defaults={
        #         'album_id': "4NZWRpoMuXaHU7csTjWdB5",
        #
        #     },
        # )

        return album


class AlbumTrack(models.Model):
    pass

class AlbumLike(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    liked_by = models.ForeignKey('users.User', on_delete=models.CASCADE)

class AlbumDislike(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    dislike_by = models.ForeignKey('users.User', on_delete=models.CASCADE)

class AlbumImpression(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

class AlbumView(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
