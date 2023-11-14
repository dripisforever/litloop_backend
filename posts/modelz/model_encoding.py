class EncodeProfile(models.Model):
    """ Encode Profile model keeps information for each profile """
    name = models.CharField(max_length=90)
    extension = models.CharField(max_length=10, choices=ENCODE_EXTENSIONS)
    resolution = models.IntegerField(choices=ENCODE_RESOLUTIONS, blank=True, null=True)
    codec = models.CharField(max_length=10, choices=CODECS, blank=True, null=True)
    description = models.TextField(blank=True, help_text="description")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["resolution"]


class Encoding(models.Model):
    """Encoding Media Instances"""
    add_date = models.DateTimeField(auto_now_add=True)
    commands = models.TextField(blank=True, help_text="commands run")
    chunk = models.BooleanField(default=False, db_index=True, help_text="is chunk?")
    chunk_file_path = models.CharField(max_length=400, blank=True)
    chunks_info = models.TextField(blank=True)
    logs = models.TextField(blank=True)
    md5sum = models.CharField(max_length=50, blank=True, null=True)
    media = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="encodings")
    media_file = models.FileField("encoding file", upload_to=encoding_media_file_path, blank=True, max_length=500)
    profile = models.ForeignKey(EncodeProfile, on_delete=models.CASCADE)
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
        if self.media_file:
            return helpers.url_from_path(self.media_file.path)
        return None

    @property
    def media_chunk_url(self):
        if self.chunk_file_path:
            return helpers.url_from_path(self.chunk_file_path)
        return None

    def save(self, *args, **kwargs):
        if self.media_file:
            cmd = ["stat", "-c", "%s", self.media_file.path]
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
        return "{0}-{1}".format(self.profile.name, self.media.title)

    def get_absolute_url(self):
        return reverse("api_get_encoding", kwargs={"encoding_id": self.id})
