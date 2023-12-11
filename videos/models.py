from django.db import models
from posts.helpers import original_media_file_path, original_thumbnail_file_path

# from mptt.models import MPTTModel, TreeForeignKey
# # from media.services import Media
#
class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='media_files/videos/')

    sprites = models.FileField(upload_to=original_thumbnail_file_path, blank=True, max_length=500)
    thumbnail = models.FileField(upload_to=original_thumbnail_file_path, blank=True, max_length=500)

    # song = models.ForeignKey(Song, on_delete=models.CASCADE, blank=True)
    # user = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True)


class VideoPlaylist(models.Model):
    videos = models.ManyToManyField(Video, through='VideoPlaylistItem')

class VideoPlaylistItem(models.Model):

    # media = models.ForeignKey(Media, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    playlist = models.ForeignKey(VideoPlaylist, on_delete=models.CASCADE)
    ordering = models.IntegerField(default=1)
