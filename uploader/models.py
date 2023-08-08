from django.db import models

# Create your models here.
# class Upload(BaseModel):
#     channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='uploads')
#     video = models.ForeignKey( Video, on_delete=models.CASCADE, related_name='uploads', null=True, blank=True,)
#     presigned_upload_urls = ArrayField(models.URLField(max_length=500), null=False, default=list, blank=True )
#     # The upload_id within the Object Storage backend itself.
#     provider_upload_id = models.CharField(max_length=400, null=True, blank=True)
#     media_type = models.CharField(max_length=500)
#     file = models.FileField(upload_to=_upload_file_upload_to, storage=STORAGE_BACKEND, null=True, blank=True )
#     status = models.CharField(max_length=20, choices=tuple((c, c) for c in UPLOAD_CHOICES), default='draft', db_index=True )
#
#     def __str__(self):
#         return (
#             f'<{self.__class__.__name__} {self.id} '
#             f'{self.channel_id} {self.status}>'
#         )
