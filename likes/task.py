# tasks.py

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from .models import Like, Post

@shared_task
def process_like(user_id, post_id):
    try:
        user = User.objects.get(pk=user_id)
        post = Post.objects.get(pk=post_id)
    except ObjectDoesNotExist:
        return

    # Check if the user has already liked the post
    if Like.objects.filter(user=user, post=post).exists():
        return

    # Create a new Like object
    like = Like(user=user, post=post)
    like.save()

    # Update the like count of the post
    post.likes = Like.objects.filter(post=post).count()
    post.save()
