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
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    caption = models.CharField(max_length=50, blank=True)
    image = models.FileField(upload_to=post_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # likes = GenericRelation(Like)
    # likes = GenericRelation(Like, related_query_name='like')
    # likes = GenericRelation(Like, related_query_name='posts')
    # likes = models.ManyToManyField(User, blank=True, related_name='likes', through=Like)
    # likes = models.ManyToManyField(Like, blank=True, related_name='likes', through=PostLike)

    # views = models.ManyToManyField(View, through="PostView", related_name="posts")
    
    # liked_users = models.ManyToManyField(User, through=Like, related_name='liked_posts')
    likes = GenericRelation(Like, related_query_name='post_likes', null=True)

    # tags = models.GenericRelation(TaggedItem, related_query_name='bookmark')
    class Meta:
        ordering: ['-updated_at']

    # def __str__(self):
    #     return str(self.author)+'s income'

    def __str__(self):
        return self.caption

    @property
    def total_likes(self):
        return self.likes.count()

    def likes_count(self):
        return self.likes.count()

    # def is_liked(self):
    #     return self.
