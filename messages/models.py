# from django.db import models
# from users.models import User
#
#
# class GroupChat(models.Model):
#     # # messages = models.ManyToManyField(Message, )
#     name = models.SlugField(max_length=20)
#     description = models.CharField()
#     members = models.ManyToManyField(User)
#
#
# class Message(models.Model):
#     parent_group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name="messages")
#     parent_user = models.ForeignKey(User, on_delete=models.SET(get_sentinal_user))
#     message_text = models.TextField()
#     date_posted = models.DateTimeField(default=timezone.localtime().now)
#     videos = models.ManyToManyField()
#     photos = models.ManyToManyField()
#     tracks = models.ManyToManyField()
#     attachments = models.ManyToManyField(Attachment)
#
#
# class Attachment(models.Model):
#     file = models.FileField(upload_to='attachments/')
#
#
# class Invite(models.Model):
#     pass
