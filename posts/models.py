from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

# from authentication.models import User
from users.models import User
from likes.models import Like
# from media.models import Media


def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'uploaded_media/post_images/post_id_{0}/{1}'.format(instance.id, filename)


class Post(models.Model):
    # media = models.ManyToManyField(Media, through="postmedia")
    # videos = models.ManyToManyField(Video, through="PostVideo")
    # tracks = models.ManyToManyField(Track, through="PostTrack")
    # photos = models.ManyToManyField(Photo, through="PostPhoto")
    # title = models.CharField(max_length=100)
    # description = models.CharField(max_length=100)

    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    caption = models.CharField(max_length=50, blank=True)
    image = models.FileField(upload_to=post_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = GenericRelation(Like, related_query_name='post_likes', null=True)
    # views = GenericRelation(View, related_query_name='post_views', null=True)

    class Meta:
        ordering: ['-updated_at']


    def __str__(self):
        return self.caption

    @property
    def total_likes(self):
        return self.likes.count()

    def likes_count(self):
        return self.likes.count()

    # def is_liked(self):
    #     return self.

# class PostVideo(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     video = models.ForeignKey(Video, on_delete=models.CASCADE)
#     ordering = models.IntegerField(default=1)
#
# class PostTrack(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     track = models.ForeignKey(Track, on_delete=models.CASCADE)
#     ordering = models.IntegerField(default=1)
#
# class PostPhoto(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
#     ordering = models.IntegerField(default=1)
