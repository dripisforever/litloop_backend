from django.db import models

# Create your models here.

class Notification(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user_noti')
    to_user = models.ForeignKey(User, related_name='to_user_noti')
    date = models.DateTimeField(auto_now_add=True, null=True)
    is_read = models.BooleanField(default=False)
    target_content_type = models.ForeignKey(ContentType, related_name='notify_target', blank=True, null=True)
    target_object_id = models.PositiveIntegerField(null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
