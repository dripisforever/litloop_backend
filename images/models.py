from django.apps import apps
from django.db import models

# from artists.models import Artist
# from albums.models import Album

# import artists.models as Artist
# import albums.models as Album

# Track = apps.get_model(app_label='tracks', model_name='Track')
# Artist = apps.get_model(app_label='artists', model_name='Artist')
# Album = apps.get_model(app_label='albums', model_name='Album')
# Like = apps.get_model(app_label='likes', model_name='Like')


class Image(models.Model):
    height = models.CharField(max_length=400)
    width = models.CharField(max_length=400)
    url = models.CharField(max_length=400)
    # url = models.FileField(upload_to=post_directory_path)
    # artist = models.ForeignKey(Artist, related_name='images')
    artist = models.ForeignKey('artists.Artist', related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    # album = models.ForeignKey(Album, related_name='images')
    album = models.ForeignKey('albums.Album', related_name='images', on_delete=models.CASCADE, null=True, blank=True)
