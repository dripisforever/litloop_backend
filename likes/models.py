# Create your models here.
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from users.models import User
# from authentication.models import User

# class Like(models.Model):
#     user = models.ForeignKey('users.User', related_name='likes', on_delete=models.CASCADE)
#
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#
#
#     date_created = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    user = models.ForeignKey('users.User', related_name='tags', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    date_created = models.DateTimeField(auto_now_add=True)


# class View(models.Model):
#     ip_address = models.GenericIPAddressField(default="", null=True, blank=True, verbose_name=_("IP"))
#     user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_('User'), null=True, blank=True)

#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('Content Type'))
#     object_id = models.PositiveIntegerField(verbose_name=_('Content ID'))
#     content_object = GenericForeignKey('content_type', 'object_id')

#     views = models.PositiveIntegerField(default=1, verbose_name=_('Total Views'), null=False)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     updated_at = models.DateTimeField(auto_now=True)

# from hitcount.models import Hit
# from django.contrib.contenttypes.models import ContentType
# content_type = ContentType.objects.get(app_label="searchroom", model="buildingcontactdetails")
#
# Hit.objects.filter(hitcount__content_type=content_type).annotate(created_date=TruncDate('created')).values('created_date').annotate(sum=Count('created_date')).values('created_date', 'sum').order_by('created_date')
#
# This show the hits per day
