# Create your models here.
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from users.models import User
# from authentication.models import User

class Like(models.Model):
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     related_name='likes',
    #     on_delete=models.CASCADE
    # )
    user = models.ForeignKey(
        'users.User',
        related_name='likes',
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date_created = models.DateTimeField(auto_now_add=True)

    # post = models.ForeignKey(
    #     Post,
    #     on_delete=models.CASCADE,
    #     related_name="likes",
    #     related_query_name="like",
    # )

    # article = models.ForeignKey(
    #     Article,
    #     on_delete=models.CASCADE,
    #     related_name="tags",
    #     related_query_name="tag",
    # )
