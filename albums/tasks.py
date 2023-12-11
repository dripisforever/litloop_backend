from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from albums.models import Album

@shared_task
def spotify_task(model_instance_id, new_value):
    try:
        obj = Album.objects.get(id=model_instance_id)
        obj.field_to_update = new_value
        obj.save()
    except ObjectDoesNotExist:
        # Handle the case where the object is not found
        pass
