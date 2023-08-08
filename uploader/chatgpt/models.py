# models.py

from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    hls_file = models.FileField(upload_to='hls/')
    created_at = models.DateTimeField(auto_now_add=True)

# models.py

class Encoding(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE)
    encoding_profile = models.ForeignKey('EncodeProfile', on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# models.py

class EncodeProfile(models.Model):
    name = models.CharField(max_length=255)
    resolution = models.CharField(max_length=10)
    bitrate = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
