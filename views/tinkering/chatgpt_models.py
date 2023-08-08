from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Add any additional fields or methods you need for your User model
    pass

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts', through='PostLike')

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} liked at {self.liked_at}'

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
