# from django.db import models
# from imagekit.models import ProcessedImageField
# from imagekit.processors import ResizeToFit
#
# from media.helpers import original_media_file_path, original_thumbnail_file_path, subtitles_file_path, category_thumb_path, encoding_media_file_path
# from media.models import Media
# from likes.models import Like
# # from likes.models import View
#
#
# class Photo(models.Model):
#     artists = models.ManyToManyField('artists.Artist', max_length=100)
#     title = models.CharField()
#     photo_file = models.FileField(upload_to="/photo")
#     thumbnail = ProcessedImageField(upload_to=original_thumbnail_file_path, processors=[ResizeToFit(width=344, height=None)], format="JPEG", options={"quality": 95}, blank=True, max_length=500)
#     uploaded_thumbnail = ProcessedImageField(upload_to=original_thumbnail_file_path, processors=[ResizeToFit(width=344, height=None)], format="JPEG", options={"quality": 85}, blank=True, max_length=500)
#     uploaded_poster = ProcessedImageField(verbose_name="Upload image", upload_to=original_thumbnail_file_path, processors=[ResizeToFit(width=720, height=None)], format="JPEG", options={"quality": 85}, blank=True, max_length=500)
#     user = models.ForeignKey("users.User", on_delete=models.CASCADE)
#     user_featured = models.BooleanField(default=False)
#     friendly_token = models.CharField(blank=True, max_length=12, db_index=True)
#     # likes = GenericRelation(Like, related_query_name='photo_likes', null=True)
#     # views = GenericRelation(View, related_query_name='photo_views', null=True)
#
#
#     def save(self, *args, **kwargs):
#
#         if not self.title:
#             self.title = self.media_file.path.split("/")[-1]
#
#         strip_text_items = ["title", "description"]
#         for item in strip_text_items:
#             setattr(self, item, strip_tags(getattr(self, item, None)))
#         self.title = self.title[:99]
#
#         # if thumbnail_time specified, keep up to single digit
#         if self.thumbnail_time:
#             self.thumbnail_time = round(self.thumbnail_time, 1)
#
#         # by default get an add_date of now
#         if not self.created_at:
#             self.created_at = timezone.now()
#
#         if not self.friendly_token:
#             # get a unique identifier
#             while True:
#                 friendly_token = helpers.produce_friendly_token()
#                 if not Media.objects.filter(friendly_token=friendly_token):
#                     self.friendly_token = friendly_token
#                     break
#
#         if self.pk:
#             # media exists
#
#             # check case where another media file was uploaded
#             if self.media_file != self.__original_media_file:
#                 # set this otherwise gets to infinite loop
#                 self.__original_media_file = self.media_file
#                 self.media_init()
#
#             # for video files, if user specified a different time
#             # to automatically grub thumbnail
#             if self.thumbnail_time != self.__original_thumbnail_time:
#                 self.__original_thumbnail_time = self.thumbnail_time
#                 self.set_thumbnail(force=True)
#         else:
#             # media is going to be created now
#             # after media is saved, post_save signal will call media_init function
#             # to take care of post save steps
#
#             self.state = helpers.get_default_state(user=self.user)
#
#         # condition to appear on listings
#         if self.state == "public" and self.encoding_status == "success" and self.is_reviewed is True:
#             self.listable = True
#         else:
#             self.listable = False
#
#         super(Media, self).save(*args, **kwargs)
#
#         # produce a thumbnail out of an uploaded poster
#         # will run only when a poster is uploaded for the first time
#         if self.uploaded_poster and self.uploaded_poster != self.__original_uploaded_poster:
#             with open(self.uploaded_poster.path, "rb") as f:
#
#                 # set this otherwise gets to infinite loop
#                 self.__original_uploaded_poster = self.uploaded_poster
#
#                 myfile = File(f)
#                 thumbnail_name = helpers.get_file_name(self.uploaded_poster.path)
#                 self.uploaded_thumbnail.save(content=myfile, name=thumbnail_name)
