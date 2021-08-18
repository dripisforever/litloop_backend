from django.db import models

# Create your models here.
#
# class Video(models.Model):
#     user = models.ForeignKey(User)
#     title = models.CharField(max_length=100)
#     original = models.FileField(upload_to=get_upload_file_name)
#     mp4_480 = models.FileField(upload_to=get_upload_file_name, blank=True, null=True)
#     mp4_720 = models.FileField(upload_to=get_upload_file_name, blank=True, null=True)
#     privacy = models.CharField(max_length=1,choices=PRIVACY, default='F')
#     pub_date = models.DateTimeField(auto_now_add=True, auto_now=False)
