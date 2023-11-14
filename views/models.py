from django.db import models
from users.models import User
from posts.models import Post
from albums.models import Album

# Create your models here.

# class View(models.Model):
#     # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
#     user = models.ForeignKey('users.User', related_name='viewed', on_delete=models.CASCADE)
#     post = models.ForeignKey('posts.Post', related_name="views", on_delete=models.CASCADE, related_query_name="view",)
#     date_created = models.DateTimeField(auto_now_add=True)
