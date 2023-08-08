import uuid
# import media.helpers as helpers
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Comment(MPTTModel):
    add_date = models.DateTimeField(auto_now_add=True)
    friendly_token = models.CharField(blank=True, max_length=27, db_index=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    text = models.TextField(help_text="text")
    uid = models.UUIDField(unique=True, default=uuid.uuid4)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, db_index=True)
    # photos = models.ManyToManyField(Photo, through="CommentPhoto")
    # videos = models.ManyToManyField(Video, through="CommentVideo")
    # tracks = models.ManyToManyField(Track, through="CommentTrack")

    # user = models.ForeignKey('users.User', related_name='comments', on_delete=models.CASCADE)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    # date_created = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ["add_date"]

    # def __str__(self):
    #     return "On {0} by {1}".format(self.media.title, self.user.username)

    def save(self, *args, **kwargs):
        strip_text_items = ["text"]
        for item in strip_text_items:
            setattr(self, item, strip_tags(getattr(self, item, None)))
        if self.text:
            self.text = self.text[: settings.MAX_CHARS_FOR_COMMENT]
        if not self.friendly_token:
            while True:
                friendly_token = helpers.produce_friendly_token(26)
                if not Comment.objects.filter(friendly_token=friendly_token):
                    self.friendly_token = friendly_token
                    break
        super(Comment, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("get_media") + "?m={0}".format(self.media.friendly_token)

    @property
    def media_url(self):
        return self.get_absolute_url()

class CommentVideo(models.Model):
    pass

class CommentAudio(models.Model):
    pass

class CommentPhoto(models.Model):
    pass

class CommentTrack(models.Model):
    pass
