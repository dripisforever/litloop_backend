from django.apps import apps
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.sites.shortcuts import get_current_site

# from artists.models import Artist
# from tracks.models import Track
# from images.models import Image
from likes.models import Like
# from media.models import Media
from albums.models import Album
from users.models import User

# import artists.models as Artist
# import tracks.models as Track
# import images.models as Image
# import likes.models  as Like

# Track = apps.get_model(app_label='tracks', model_name='Track')
# Artist = apps.get_model(app_label='artists', model_name='Artist')
# Album = apps.get_model(app_label='albums', model_name='Album')
# Like = apps.get_model(app_label='likes', model_name='Like')



class Playlist(models.Model):

    id = models.BigAutoField(primary_key=True)
    # media = models.ManyToManyField(Media, through='PlaylistTrack')
    videos = models.ManyToManyField(Video, through='PlaylistVideo')
    # tracks = models.ManyToManyField(Track,  through='PlaylistTrack')
    # id = models.CharField(max_length=400, primary_key=True)
    # name = models.CharField(max_length=400)
    # playlist_uri = models.CharField(max_length=400)
    # artists = models.ManyToManyField('artists.Artist', related_name='albums')
    # images = models.ManyToManyField(Image, related_name='albums')
    # likes = GenericRelation(Like, related_query_name='album_likes', null=True)
    # likes = GenericRelation('likes.Like', related_query_name='album_likes', null=True, on_delete=models.CASCADE)
    # likes = GenericRelation(Like, related_query_name='album_likes', null=True, on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    # faves = models.ManyToManyField('users.User', related_name='album_user', blank=True, through=TweetLike)
    # album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    # author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    # @classmethod
    # def create(cls, **kwargs):
    #
    #     from artists.models import Artist
    #     from tracks.models import Track
    #     from images.models import Image
    #     # current_site = get_current_site(request).domain
    #
    #     playlist, created = cls.objects.get_or_create(
    #         playlist_uri = kwargs['id'],
    #         name = kwargs['name'],
    #     )
    #
    #     for artist_data in kwargs['artists']:
    #
    #         artist, created = Artist.objects.get_or_create(
    #             artist_uri = artist_data['id'],
    #             name = artist_data['name'],
    #         )
    #         album.artists.add(artist)
    #
    #     for track_data in kwargs['tracks']['items']:
    #
    #         track, created = Track.objects.get_or_create(
    #             track_uri = track_data["id"],
    #             name = track_data["name"],
    #             album_id = album.id,
    #             track_number = track_data['track_number'],
    #             # href = current_site + "track/" + kwargs['items']['id'] + "/",
    #         )
    #         album.tracks.add(track)
    #
    #         for artist_data in track_data['artists']:
    #             artist, created = Artist.objects.get_or_create(
    #                 artist_uri = artist_data['id'],
    #                 name = artist_data['name'],
    #             )
    #             track.artists.add(artist)
    #
    #
    #     for images_data in kwargs['images']:
    #         # extract_id_from_url = images_data["url"]
    #         image, created = Image.objects.get_or_create(
    #             url = images_data["url"],
    #             height = images_data["height"],
    #             width = images_data["width"],
    #             album_id = album.id,
    #
    #         )
    #
    #
    #     # album = cls.objects.update_or_create(
    #     #     id=1,
    #     #     defaults={
    #     #         'album_id': "4NZWRpoMuXaHU7csTjWdB5",
    #     #
    #     #     },
    #     # )
    #
    #     return album
    def __str__(self):
        return self.title

    @property
    def media_count(self):
        return self.media.count()

    def get_absolute_url(self, api=False):
        if api:
            return reverse("api_get_playlist", kwargs={"friendly_token": self.friendly_token})
        else:
            return reverse("get_playlist", kwargs={"friendly_token": self.friendly_token})

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def api_url(self):
        return self.get_absolute_url(api=True)

    def user_thumbnail_url(self):
        if self.user.logo:
            return helpers.url_from_path(self.user.logo.path)
        return None

    def set_ordering(self, media, ordering):
        if media not in self.media.all():
            return False
        pm = PlaylistTrack.objects.filter(playlist=self, media=media).first()
        if pm and isinstance(ordering, int) and 0 < ordering:
            pm.ordering = ordering
            pm.save()
            return True
        return False

    def save(self, *args, **kwargs):
        strip_text_items = ["title", "description"]
        for item in strip_text_items:
            setattr(self, item, strip_tags(getattr(self, item, None)))
        self.title = self.title[:99]

        if not self.friendly_token:
            while True:
                friendly_token = helpers.produce_friendly_token()
                if not Playlist.objects.filter(friendly_token=friendly_token):
                    self.friendly_token = friendly_token
                    break
        super(Playlist, self).save(*args, **kwargs)

    @property
    def thumbnail_url(self):
        pm = self.playlistmedia_set.first()
        if pm and pm.media.thumbnail:
            return helpers.url_from_path(pm.media.thumbnail.path)
        return None


class PlaylistTrack(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    ordering = models.IntegerField(default=1)
