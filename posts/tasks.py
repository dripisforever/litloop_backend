# tasks.py

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
# from views.models import View
from posts.models import Post, PostView



@shared_task
def process_view(user_id, post_id):
    try:
        user = User.objects.get(pk=user_id)
        post = Post.objects.get(pk=post_id)
    except ObjectDoesNotExist:
        return

    # Check if the user has already viewed the post
    if PostView.objects.filter(user=user, post=post).exists():
        return

    # Create a new View object
    view = PostView(user=user, post=post)
    view.save()

    # Update the like count of the post
    # post.views = View.objects.filter(post=post).count()
    # post.save()
