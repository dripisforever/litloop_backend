from django.apps import apps
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.sites.shortcuts import get_current_site

from artists.models import Artist
from tracks.models import Track
from images.models import Image
from albums.models import Album
from users.models import User
# from likes.models import Like
# from media.models import Media


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
    # videos = models.ManyToManyField(Video, through='PlaylistVideo')
    # tracks = models.ManyToManyField(Track, through='PlaylistTrack')
    # albums = models.ManyToManyField(Album, through='PlaylistAlbum')
    # photos = models.ManyToManyField(Photo, through='PlaylistPhoto')

    # id = models.CharField(max_length=400, primary_key=True)
    # name = models.CharField(max_length=400)
    # playlist_uri = models.CharField(max_length=400)
    # artists = models.ManyToManyField('artists.Artist', related_name='albums')

    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    # likes = models.ManyToManyField('users.User', related_name='liked_playlists', blank=True, through=PlaylistLike)
    # album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    # author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)


    # Pinned position
    # user = models.ForeignKey(User, relaed)
    # ordering = models.IntegerField(default=1) # REFERENCE MEDIACMS
    # pinned = models.BooleanField(default=False) # REFERENCE https://stackoverflow.com/questions/46943893/pin-only-one-post-in-django-powered-blog
    # pin_position = models.IntegerField()
    # rank = models.Integerfield(default=0) # REFERENCE https://stackoverflow.com/questions/66570706/how-to-pin-posts-in-django
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


# class PlaylistTrack(models.Model):
#     media = models.ForeignKey(Media, on_delete=models.CASCADE)
#     track = models.ForeignKey(Track, on_delete=models.CASCADE)
#     playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
#     ordering = models.IntegerField(default=1)
#
# class PlaylistVideo(models.Model):
#     media = models.ForeignKey(Media, on_delete=models.CASCADE)
#     video = models.ForeignKey(Video, on_delete=models.CASCADE)
#     playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
#     ordering = models.IntegerField(default=1)
