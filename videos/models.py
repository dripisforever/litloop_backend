# from django.db import models
# from mptt.models import MPTTModel, TreeForeignKey
# # from media.services import Media
#
# class Video(models.Model):
#     # likes = GenericRelation(Like, related_query_name='post_likes', null=True)
#     # dislikes = GenericRelation(Dislike, related_query_name='post_dislikes', null=True)
#     # views = GenericRelation(View, related_query_name='post_views', null=True)
#     video_file = models.FileField(upload_to='/videos')
#     title = models.CharField(max_length=100)
#     description = models.CharField(max_length=100)
#     song = models.ForeignKey(Song, on_delete=models.CASCADE, blank=True)
#
#
# class VideoPlaylist(models.Model):
#     videos = models.ManyToManyField(Video, through='VideoPlaylistItem')
#
# class VideoPlaylistItem(models.Model):
#
#     # media = models.ForeignKey(Media, on_delete=models.CASCADE)
#     video = models.ForeignKey(Video, on_delete=models.CASCADE)
#     playlist = models.ForeignKey(VideoPlaylist, on_delete=models.CASCADE)
#     ordering = models.IntegerField(default=1)
