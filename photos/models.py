import uuid

from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from posts.helpers import original_media_file_path, original_thumbnail_file_path
# from likes.models import Like



class Photo(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.TextField(blank=True, null=True)
    photo_file = models.FileField(upload_to="media_files/photos/")

    thumbnail = ProcessedImageField(upload_to=original_thumbnail_file_path, processors=[ResizeToFit(width=344, height=None)], format="JPEG", options={"quality": 95}, blank=True, max_length=500)
    uploaded_thumbnail = ProcessedImageField(upload_to=original_thumbnail_file_path, processors=[ResizeToFit(width=344, height=None)], format="JPEG", options={"quality": 85}, blank=True, max_length=500)
    uploaded_poster = ProcessedImageField(verbose_name="Upload image", upload_to=original_thumbnail_file_path, processors=[ResizeToFit(width=720, height=None)], format="JPEG", options={"quality": 85}, blank=True, max_length=500)


    user_featured = models.BooleanField(default=False)
    friendly_token = models.CharField(blank=True, max_length=12, db_index=True)
    # likes = GenericRelation(Like, related_query_name='photo_likes', null=True)
    # views = GenericRelation(View, related_query_name='photo_views', null=True)

    # keep track if media file has changed, on saves
    __original_photo_file = None
    __original_thumbnail_time = None
    __original_uploaded_poster = None

    def save(self, *args, **kwargs):

        if not self.title:
            self.title = self.photo_file.path.split("/")[-1]

        strip_text_items = ["title", "description"]
        for item in strip_text_items:
            setattr(self, item, strip_tags(getattr(self, item, None)))
        self.title = self.title[:99]

        # if thumbnail_time specified, keep up to single digit
        if self.thumbnail_time:
            self.thumbnail_time = round(self.thumbnail_time, 1)

        # by default get an add_date of now
        if not self.created_at:
            self.created_at = timezone.now()

        if not self.friendly_token:
            # get a unique identifier
            while True:
                friendly_token = helpers.produce_friendly_token()
                if not Photo.objects.filter(friendly_token=friendly_token):
                    self.friendly_token = friendly_token
                    break

        if self.pk:
            # media exists

            # check case where another media file was uploaded
            if self.photo_file != self.__original_photo_file:
                # set this otherwise gets to infinite loop
                self.__original_photo_file = self.photo_file
                self.media_init()

            # for video files, if user specified a different time
            # to automatically grub thumbnail
            if self.thumbnail_time != self.__original_thumbnail_time:
                self.__original_thumbnail_time = self.thumbnail_time
                self.set_thumbnail(force=True)
        else:
            # media is going to be created now
            # after media is saved, post_save signal will call media_init function
            # to take care of post save steps

            self.state = helpers.get_default_state(user=self.user)

        # condition to appear on listings
        if self.state == "public" and self.encoding_status == "success" and self.is_reviewed is True:
            self.listable = True
        else:
            self.listable = False

        super(Photo, self).save(*args, **kwargs)

        # produce a thumbnail out of an uploaded poster
        # will run only when a poster is uploaded for the first time
        if self.uploaded_poster and self.uploaded_poster != self.__original_uploaded_poster:
            with open(self.uploaded_poster.path, "rb") as f:

                # set this otherwise gets to infinite loop
                self.__original_uploaded_poster = self.uploaded_poster

                myfile = File(f)
                thumbnail_name = helpers.get_file_name(self.uploaded_poster.path)
                self.uploaded_thumbnail.save(content=myfile, name=thumbnail_name)

    def media_init(self):
        """Normally this is called when a media is uploaded
        Performs all related tasks, as check for media type,
        video duration, encode
        """

        self.set_media_type()
        if self.media_type == "video":
            self.set_thumbnail(force=True)
            self.produce_sprite_from_video()
            self.encode()

            # Video.objects.create(
            #     media=self,
            #     title=self.title,
            #     description=self.description,
            #     file=self.media_file,
            #     hls_file=self.hls_file,
            # )

        elif self.media_type == "image":
            self.set_thumbnail(force=True)

            # Photo.objects.create(
            #     media=self,
            #     title=self.title
            # )

        # elif self.media_type == "audio":
        #     self.set_thumbnail(force=True)

            # Track.objects.create(
            #     media=self,
            #     title=self.title,
            #     description=self.description
            # )

        return True


class PhotoLike(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    liked_by = models.ForeignKey('users.User', on_delete=models.CASCADE)

class PhotoDislike(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    dislike_by = models.ForeignKey('users.User', on_delete=models.CASCADE)

class PhotoImpression(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

class PhotoView(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)


class PhotoAlbum(models.Model):
    """PhotoAlbums model"""

    add_date = models.DateTimeField(auto_now_add=True, db_index=True)
    description = models.TextField(blank=True, help_text="description")
    friendly_token = models.CharField(blank=True, max_length=12, db_index=True)
    photo = models.ManyToManyField(Photo, through="PhotoAlbumItem", blank=True)
    title = models.CharField(max_length=100, db_index=True)
    uid = models.UUIDField(unique=True, default=uuid.uuid4)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, db_index=True, related_name="photoalbums")

    def __str__(self):
        return self.title

    @property
    def photo_count(self):
        return self.photo.count()

    def get_absolute_url(self, api=False):
        if api:
            return reverse("api_get_photoalbum", kwargs={"friendly_token": self.friendly_token})
        else:
            return reverse("get_playlist", kwargs={"friendly_token": self.friendly_token})

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def api_url(self):
        return self.get_absolute_url(api=True)

    def user_thumbnail_url(self):
        if self.user.logo:
            return helpers.url_from_path(self.user.logo.path)
        return None

    def set_ordering(self, photo, ordering):
        if photo not in self.photo.all():
            return False
        pa = PhotoAlbum.objects.filter(photo_album=self, photo=photo).first()
        if pa and isinstance(ordering, int) and 0 < ordering:
            pa.ordering = ordering
            pa.save()
            return True
        return False

    def save(self, *args, **kwargs):
        strip_text_items = ["title", "description"]
        for item in strip_text_items:
            setattr(self, item, strip_tags(getattr(self, item, None)))
        self.title = self.title[:99]

        if not self.friendly_token:
            while True:
                friendly_token = helpers.produce_friendly_token()
                if not PhotoAlbum.objects.filter(friendly_token=friendly_token):
                    self.friendly_token = friendly_token
                    break
        super(PhotoAlbum, self).save(*args, **kwargs)

    @property
    def thumbnail_url(self):
        pai = self.photoalbumitem_set.first()
        if pai and pai.photo.thumbnail:
            return helpers.url_from_path(pai.photo.thumbnail.path)
        return None


class PhotoAlbumItem(models.Model):
    """Helper model to store playlist specific media"""

    action_date = models.DateTimeField(auto_now=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    photo_album = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE)
    ordering = models.IntegerField(default=1)

    class Meta:
        ordering = ["ordering", "-action_date"]
