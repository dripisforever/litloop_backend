from typing import TYPE_CHECKING, Tuple

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest

from posts.models import PostLike
from likes.signals import object_liked, object_unliked
from likes.selectors import get_user_likes

from posts.models import Post

if TYPE_CHECKING:
    from django.db.models import Model

User = get_user_model()

__all__ = (
    'toggle',
    'get_user_likes_count',
    'get_object_likes_count',
    'is_object_liked_by_user',
    'send_signals'
)


def toggle(user, content_type, object_id):
    """
    Class method to like-dislike object
    """
    obj, created = PostLike.objects.get_or_create(
        user=user,
        content_type=content_type,
        object_id=object_id
    )

    if not created:
        obj.delete()

    return obj, created


def toggle_post(user, content_type, object_id):
    """
    Class method to like-dislike object
    """
    obj, created = Post.objects.get_or_create(
        # user=user,
        # content_type=content_type,
        # object_id=object_id
    )

    if not created:
        obj.delete()

    return obj, created


def get_user_likes_count(*, user, content_type):
    """
    Returns count of likes for a given user.
    """
    if not user.is_authenticated:
        return 0

    return (
        get_user_likes(
            user=user,
            content_type=content_type
        )
        .count()
    )


def get_object_likes_count(obj):
    """
    Returns count of likes for a given object.
    """
    return (
        PostLike.objects
        .filter(
            content_type=(
                ContentType.objects.get_for_model(obj)
            ),
            object_id=obj.pk
        )
        .count()
    )


def is_object_liked_by_user(obj, user):
    """
    Checks if a given object is liked by a given user.
    """
    if not user.is_authenticated:
        return False

    return (
        PostLike.objects
        .filter(
            content_type=(
                ContentType.objects.get_for_model(obj)
            ),
            object_id=obj.pk,
            user=user
        )
        .exists()
    )


def send_signals(created, request, like, obj):
    """
    Sends signals when object was liked and unliked.
    """
    if created:
        object_liked.send(
            sender=PostLike,
            like=like,
            request=request
        )
    else:
        object_unliked.send(
            sender=PostLike,
            object=obj,
            request=request
        )


def is_fan(obj, user):
    """Check whether a user liked an `obj` or not.
    """
    if not user.is_authenticated:
        return False

    obj_type = ContentType.objects.get_for_model(obj)

    likes = PostLike.objects.filter(
        content_type=obj_type,
        object_id=obj.id,
        user=user
    )

    return likes.exists()







    #











    #



















    #
