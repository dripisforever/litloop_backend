import tempfile


from django.db import models
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_delete
from django.dispatch import receiver
from django.utils.html import strip_tags

from users.models import User
from photos.models import Photo
from videos.models import Video
from tracks.models import Track
from playlists.models import Playlist

from .helpers import (
    MEDIA_ENCODING_STATUS,


    ENCODE_EXTENSIONS,
    ENCODE_RESOLUTIONS,
    CODECS,
    ENCODE_EXTENSIONS_KEYS,
    ENCODE_RESOLUTIONS_KEYS,
    encoding_media_file_path
)

def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'uploaded_media/post_images/post_id_{0}/{1}'.format(instance.id, filename)


class Post(models.Model):

    videos = models.ManyToManyField(Video, through="PostVideo")
    tracks = models.ManyToManyField(Track, through="PostTrack")
    photos = models.ManyToManyField(Photo, through="PostPhoto")
    playlists = models.ManyToManyField(Playlist, through="PostPlaylist")
    # likes = models.ManyToManyField(User, through="PostLike")

    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)

    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    caption = models.CharField(max_length=50, blank=True)
    image = models.FileField(upload_to=post_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    likes = models.ManyToManyField(User, through='PostLike', blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, through='PostDislike', blank=True, related_name='dislikes')
    views = models.ManyToManyField(User, through='PostView', blank=True, related_name='views')
    impressions = models.ManyToManyField(User, through='PostImpression', blank=True, related_name='impressions')


    class Meta:
        ordering: ['-updated_at']


    def __str__(self):
        return self.caption

    @property
    def total_likes(self):
        return self.likes.count()

    def likes_count(self):
        return self.likes.count()

    def views_count(self):
        return self.views.count()

    def save(self, *args, **kwargs):
        strip_text_items = ["title", "description"]
        for item in strip_text_items:
            setattr(self, item, strip_tags(getattr(self, item, None)))
        self.title = self.title[:99]

        if not self.friendly_token:
            while True:
                friendly_token = helpers.produce_friendly_token()
                if not Post.objects.filter(friendly_token=friendly_token):
                    self.friendly_token = friendly_token
                    break
        super(Post, self).save(*args, **kwargs)
    # def is_liked(self):
    #     return self.


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)

class PostDislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    dislike_by = models.ForeignKey(User, on_delete=models.CASCADE)

class PostImpression(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class PostPhoto(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    photo = models.ForeignKey('photos.Photo', on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

class PostVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video = models.ForeignKey('videos.Video', on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

class PostTrack(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    track = models.ForeignKey('tracks.Track', on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

class PostPlaylist(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    playlist = models.ForeignKey('playlists.Playlist', on_delete=models.CASCADE)
    order = models.IntegerField(default=1)


class EncodeProfile(models.Model):
    """ Encode Profile model keeps information for each profile """
    name = models.CharField(max_length=90, blank=True)
    extension = models.CharField(max_length=10, choices=ENCODE_EXTENSIONS)
    resolution = models.IntegerField(choices=ENCODE_RESOLUTIONS, blank=True, null=True)
    codec = models.CharField(max_length=10, choices=CODECS, blank=True, null=True)
    description = models.TextField(blank=True, help_text="description")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["resolution"]


class VideoEncoding(models.Model):
    """Encoding Media Instances"""
    add_date = models.DateTimeField(auto_now_add=True)
    commands = models.TextField(blank=True, help_text="commands run")
    chunk = models.BooleanField(default=False, db_index=True, help_text="is chunk?")
    chunk_file_path = models.CharField(max_length=400, blank=True)
    chunks_info = models.TextField(blank=True)
    logs = models.TextField(blank=True)
    md5sum = models.CharField(max_length=50, blank=True, null=True)

    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="encodings")
    profile = models.ForeignKey(EncodeProfile, on_delete=models.CASCADE)
    encoding_file = models.FileField("encoding file", upload_to=encoding_media_file_path, blank=True, max_length=500)

    progress = models.PositiveSmallIntegerField(default=0)
    update_date = models.DateTimeField(auto_now=True)
    retries = models.IntegerField(default=0)
    size = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=MEDIA_ENCODING_STATUS, default="pending")
    temp_file = models.CharField(max_length=400, blank=True)
    task_id = models.CharField(max_length=100, blank=True)
    total_run_time = models.IntegerField(default=0)
    worker = models.CharField(max_length=100, blank=True)

    @property
    def media_encoding_url(self):
        if self.encoding_file:
            return helpers.url_from_path(self.encoding_file.path)
        return None

    @property
    def media_chunk_url(self):
        if self.chunk_file_path:
            return helpers.url_from_path(self.chunk_file_path)
        return None

    def save(self, *args, **kwargs):
        if self.encoding_file:
            cmd = ["stat", "-c", "%s", self.encoding_file.path]
            stdout = helpers.run_command(cmd).get("out")
            if stdout:
                size = int(stdout.strip())
                self.size = helpers.show_file_size(size)
        if self.chunk_file_path and not self.md5sum:
            cmd = ["md5sum", self.chunk_file_path]
            stdout = helpers.run_command(cmd).get("out")
            if stdout:
                md5sum = stdout.strip().split()[0]
                self.md5sum = md5sum

        super(Encoding, self).save(*args, **kwargs)

    def set_progress(self, progress, commit=True):
        if isinstance(progress, int):
            if 0 <= progress <= 100:
                self.progress = progress
                self.save(update_fields=["progress"])
                return True
        return False

    def __str__(self):
        return "{0}-{1}".format(self.profile.name, self.video.title)

    def get_absolute_url(self):
        return reverse("api_get_encoding", kwargs={"encoding_id": self.id})


@receiver(post_save, sender=VideoEncoding)
def encoding_file_save(sender, instance, created, **kwargs):
    """Performs actions on encoding file delete
    For example, if encoding is a chunk file, with encoding_status success,
    perform a check if this is the final chunk file of a media, then
    concatenate chunks, create final encoding file and delete chunks
    """

    if instance.chunk and instance.status == "success":
        # a chunk got completed

        # check if all chunks are OK
        # then concatenate to new Encoding - and remove chunks
        # this should run only once!
        if instance.encoding_file:
            try:
                orig_chunks = json.loads(instance.chunks_info).keys()
            except BaseException:
                instance.delete()
                return False

            chunks = VideoEncoding.objects.filter(
                video=instance.video,
                profile=instance.profile,
                chunks_info=instance.chunks_info,
                chunk=True,
            ).order_by("add_date")

            complete = True

            # perform validation, make sure everything is there
            for chunk in orig_chunks:
                if not chunks.filter(chunk_file_path=chunk):
                    complete = False
                    break

            for chunk in chunks:
                if not (chunk.encoding_file and chunk.encoding_file.path):
                    complete = False
                    break

            if complete:
                # concatenate chunks and create final encoding file
                chunks_paths = [f.encoding_file.path for f in chunks]

                with tempfile.TemporaryDirectory(dir=settings.TEMP_DIRECTORY) as temp_dir:
                    seg_file = helpers.create_temp_file(suffix=".txt", dir=temp_dir)
                    tf = helpers.create_temp_file(suffix=".{0}".format(instance.profile.extension), dir=temp_dir)
                    with open(seg_file, "w") as ff:
                        for f in chunks_paths:
                            ff.write("file {}\n".format(f))
                    cmd = [
                        settings.FFMPEG_COMMAND,
                        "-y",
                        "-f",
                        "concat",
                        "-safe",
                        "0",
                        "-i",
                        seg_file,
                        "-c",
                        "copy",
                        "-pix_fmt",
                        "yuv420p",
                        "-movflags",
                        "faststart",
                        tf,
                    ]
                    stdout = helpers.run_command(cmd)

                    encoding = VideoEncoding(
                        video=instance.video,
                        profile=instance.profile,
                        status="success",
                        progress=100,
                    )
                    all_logs = "\n".join([st.logs for st in chunks])
                    encoding.logs = "{0}\n{1}\n{2}".format(chunks_paths, stdout, all_logs)
                    workers = list(set([st.worker for st in chunks]))
                    encoding.worker = json.dumps({"workers": workers})

                    start_date = min([st.add_date for st in chunks])
                    end_date = max([st.update_date for st in chunks])
                    encoding.total_run_time = (end_date - start_date).seconds
                    encoding.save()

                    with open(tf, "rb") as f:
                        myfile = File(f)
                        output_name = "{0}.{1}".format(
                            helpers.get_file_name(instance.video.video_file.path),
                            instance.profile.extension,
                        )
                        encoding.encoding_file.save(content=myfile, name=output_name)

                    # encoding is saved, deleting chunks
                    # and any other encoding that might exist
                    # first perform one last validation
                    # to avoid that this is run twice
                    if (
                        len(orig_chunks)
                        == VideoEncoding.objects.filter(  # noqa
                            media=instance.video,
                            profile=instance.profile,
                            chunks_info=instance.chunks_info,
                        ).count()
                    ):
                        # if two chunks are finished at the same time, this
                        # will be changed
                        who = VideoEncoding.objects.filter(video=encoding.video, profile=encoding.profile).exclude(id=encoding.id)
                        who.delete()
                    else:
                        encoding.delete()
                    if not VideoEncoding.objects.filter(chunks_info=instance.chunks_info):
                        # TODO: in case of remote workers, files should be deleted
                        # example
                        # for worker in workers:
                        #    for chunk in json.loads(instance.chunks_info).keys():
                        #        remove_media_file.delay(media_file=chunk)
                        for chunk in json.loads(instance.chunks_info).keys():
                            helpers.rm_file(chunk)
                    instance.video.post_encode_actions(encoding=instance, action="add")

    elif instance.chunk and instance.status == "fail":
        encoding = VideoEncoding(video=instance.video, profile=instance.profile, status="fail", progress=100)

        chunks = VideoEncoding.objects.filter(video=instance.video, chunks_info=instance.chunks_info, chunk=True).order_by("add_date")

        chunks_paths = [f.encoding_file.path for f in chunks]

        all_logs = "\n".join([st.logs for st in chunks])
        encoding.logs = "{0}\n{1}".format(chunks_paths, all_logs)
        workers = list(set([st.worker for st in chunks]))
        encoding.worker = json.dumps({"workers": workers})
        start_date = min([st.add_date for st in chunks])
        end_date = max([st.update_date for st in chunks])
        encoding.total_run_time = (end_date - start_date).seconds
        encoding.save()

        who = VideoEncoding.objects.filter(video=encoding.video, profile=encoding.profile).exclude(id=encoding.id)

        who.delete()
        # TODO: merge with above if, do not repeat code
    else:
        if instance.status in ["fail", "success"]:
            instance.video.post_encode_actions(encoding=instance, action="add")

        encodings = set([encoding.status for encoding in VideoEncoding.objects.filter(video=instance.video)])
        if ("running" in encodings) or ("pending" in encodings):
            return


@receiver(post_delete, sender=VideoEncoding)
def encoding_file_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Encoding` object is deleted.
    """

    if instance.encoding_file:
        helpers.rm_file(instance.encoding_file.path)
        if not instance.chunk:
            instance.video.post_encode_actions(encoding=instance, action="delete")
    # delete local chunks, and remote chunks + media file. Only when the
    # last encoding of a media is complete
