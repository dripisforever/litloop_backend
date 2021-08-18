from django.apps import apps
from django.db import models
# from django.contrib.contenttypes.fields import GenericRelation

# from albums.models import Album
# from tracks.models import Track

# import albums.models as Album
# import tracks.models as Track

# Track = apps.get_model(app_label='tracks', model_name='Track')
# Artist = apps.get_model(app_label='artists', model_name='Artist')
# Album = apps.get_model(app_label='albums', model_name='Album')
# Like = apps.get_model(app_label='likes', model_name='Like')

class Artist(models.Model):
    name = models.CharField(max_length=300)
    artist_uri = models.CharField(max_length=300)
    # album = models.ManyToManyField(Album, related_name='artists')
    # albums = models.ManyToManyField('albums.Album', related_name='artists')
    # album = models.ManyToManyField('albums.Album', related_name='artists', on_delete=models.CASCADE)
    # track = models.ManyToManyField(Track, related_name='artists')
    # tracks = models.ManyToManyField('tracks.Track', related_name='artists')
    # track = models.ManyToManyField('tracks.Track', related_name='artists', on_delete=models.CASCADE)
    # images = models.ManyToManyField(Image, related_name='artists')

    @classmethod
    def create(cls, **kwargs):
        from artists.models import Artist
        from albums.models import Album
        from tracks.models import Track
        from images.models import Image

        artist, created = cls.objects.get_or_create(
            artist_uri = kwargs['id'],
            name = kwargs['name']
        )

        # for track_data in kwargs['tracks']:
        #
        #     track, created = Track.objects.get_or_create(
        #         artist_uri = artists_data["id"],
        #         name = artists_data["name"]
        #
        #     )
        #     artist.tracks.add(artist)
        #
        # for album_data in kwargs['album']:
        #
        #     album, created = Album.objects.get_or_create(
        #         album_uri = album_data["id"],
        #         name = album_data["name"]
        #
        #     )
        #     artist.albums.add(album)

        for images_data in kwargs['images']:
            # extract_id_from_url = images_data["url"]
            image, created = Image.objects.get_or_create(
                url = images_data["url"],
                height = images_data["height"],
                width = images_data["width"],
                artist_id = artist.id,
            )
            
        #
        return artist
