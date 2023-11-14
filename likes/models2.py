# Create your models here.
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from users.models import User

class Like(models.Model):

    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE, related_query_name="like",)
    date_created = models.DateTimeField(auto_now_add=True)


# class Post(models.Model):
#     likes = models.ManyToManyField(User)


class Reaction(models.Model):
    reaction_types = [
        ('LO', 'Love'),
        ('LI', 'Like'),
        ('HA', 'Haha'),
        ('WA', 'Wow'),
        ('SA', 'Sad'),
        ('AN', 'Angry'),
    ]
    reaction_type = models.CharField(max_length=6, choices=reaction_types)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions', related_query_name='reaction',
                             null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reactions',
                                related_query_name='reaction', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions', related_query_name='reaction')

    class Meta:
        unique_together = [['post', 'user'], ['comment', 'user']]

    def __str__(self):
        return self.reaction_type

    objects = models.Manager()
    postReactions = PostManager()


class Reaction(models.Model):
    REACT_TYPES = [
        ('LO', 'Love'),
        ('LI', 'Like'),
        ('HA', 'Haha'),
        ('WA', 'Wow'),
        ('SA', 'Sad'),
        ('AN', 'Angry'),
    ]
    user = models.ForeignKey(User)
    react_type = models.CharField(max_length=100, choices=REACT_TYPES, default='NO')
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
       super(Reaction, self).save(*args, **kwargs)
       Notification(from_user = self.user, to_user = self.content_object.user, notification_type = Notification.LIKED, target_content_type = self.content_type, target_object_id = self.object_id).save()


class Notification(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user_noti')
    to_user = models.ForeignKey(User, related_name='to_user_noti')
    date = models.DateTimeField(auto_now_add=True, null=True)
    is_read = models.BooleanField(default=False)
    target_content_type = models.ForeignKey(ContentType, related_name='notify_target', blank=True, null=True)
    target_object_id = models.PositiveIntegerField(null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
