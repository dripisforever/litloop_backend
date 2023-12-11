from django.db import models
from users.models import User

# Create your models here.
class Movie(models.Model):
    tmdb_id = models.IntegerField(null=True, blank=True)
    imdb_id = models.IntegerField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    movie_file = models.FileField(upload_to='uploaded_media/movie', null=True, blank=True)
    poster = models.FileField(upload_to='uploaded_media/movie/poster', null=True, blank=True)

    views = models.ManyToManyField(User, through='MovieView', blank=True, related_name='movie_views')
    impressions = models.ManyToManyField(User, through='MovieImpression', blank=True, related_name='movie_impressions')

    # @classmethod
    # def create(cls, **kwargs):

        # from artists.models import Artist
        # from tracks.models import Track
        # from images.models import Image

        # current_site = get_current_site(request).domain

        # movie, created = cls.objects.get_or_create(
        #     tmdb_id = kwargs['id'],
        #     title = kwargs['name'],
        # )


        # for images_data in kwargs['images']:
        #     # extract_id_from_url = images_data["url"]
        #     image, created = Image.objects.get_or_create(
        #         url = images_data["url"],
        #         height = images_data["height"],
        #         width = images_data["width"],
        #         album_id = album.id,
        #
        #     )
        #
        #
        # return movie


class MovieImpression(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

class MovieView(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
