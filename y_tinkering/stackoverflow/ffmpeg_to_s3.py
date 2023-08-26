# REFERENCE: https://stackoverflow.com/questions/14776314/can-i-convert-a-django-video-upload-from-a-form-using-ffmpeg-before-storing-the
from django.contrib.auth.models import User

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    new_file_name = "remove%s.%s" % (uuid.uuid4(), ext)
    return '/'.join(['videos', instance.teacher.username, new_file_name])

class BroadcastUpload(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Title'))
    description = models.TextField(max_length=100, verbose_name=_('Description'))
    teacher = models.ForeignKey(User, null=True, blank=True, related_name='teacher')
    created_date = models.DateTimeField(auto_now_add=True)
    video_upload = models.FileField(upload_to=content_file_name)
    #flvfilename = models.CharField(max_length=100, null=True, blank=True)
    video_flv = models.FileField(upload_to='flv', blank=True)
    #videothumbnail = models.CharField(max_length=100, null=True, blank=True)
    video_thumbnail = models.FileField(upload_to='thumbs', blank=True)

    def __unicode__(self):
        return u'%s - %s' % (self.title, self.teacher)

    def save(self, *args, **kwargs):
        # optional parameter to indicate whether perform
        # conversion or not. Defaults to True
        do_conversion = kwargs.pop('do_conversion', True)

        # do something only when the entry is created
        if not self.pk:
            super(BroadcastUpload, self).save(*args, **kwargs)

        # do something every time the entry is updated
        if do_conversion:
            ffmpeg_image.delay(self.pk)
            convert_flv.delay(self.pk)

        # then call the parent save:
        super(BroadcastUpload, self).save(*args, **kwargs)

from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile

@task
def convert_flv(video_id):
    video = BroadcastUpload.objects.get(pk=video_id)
    print "ID: %s" % video.id
    id = video.id
    print "VIDEO NAME: %s" % video.video_upload.name
    teacher = video.teacher
    print "TEACHER: %s" % teacher
    filename = video.video_upload
    #sourcefile = "%s%s" % (settings.MEDIA_URL, filename)
    sourcefile = video.video_upload.url
    # ffmpeg cannot deal with https?
    sourcefile = sourcefile.replace("https","http")
    print "sourcefile: %s" % sourcefile

    # temporary output image
    OUTPUT_VIDEO_EXT = 'flv'
    OUTPUT_VIDEO_CONTENT_TYPE = 'video/flv'
    f_out = tempfile.NamedTemporaryFile(suffix=".%s"%OUTPUT_VIDEO_EXT, delete=False)
    tmp_output_video = f_out.name

    #ffmpeg = "ffmpeg -i '%s' -qscale 0 -ar 44100 '%s'" % (sourcefile, vidfilename)
    ffmpeg = "ffmpeg -y -i '%s' -qscale 0 -ar 44100 '%s'" % (sourcefile, tmp_output_video)
    print "convert_flv: %s" % ffmpeg
    try:
        ffmpegresult = subprocess.call(ffmpeg, shell=True)
        #also tried separately with following line:
        #ffmpegresult = commands.getoutput(ffmpeg)
        print "---------------FFMPEG---------------"
        print "FFMPEGRESULT: %s" % ffmpegresult
    except Exception as e:
        ffmpegresult = None
        #print("Failed to convert video file %s to %s" % (sourcefile, targetfile))
        print("Failed to convert video file %s to %s" % (sourcefile, tmp_output_video))
        #print(traceback.format_exc())
        print "Error: %s" % e

    #vidfilename = "%s_%s.flv" % (teacher, video.id)
    vidfilename = "%s_%s.%s" % (teacher, video.id, OUTPUT_VIDEO_EXT)
    #targetfile = "%svideos/flv/%s" % (settings.MEDIA_URL, vidfilename)

    # prepare an object with the generated temporary image
    suf = SimpleUploadedFile(
        vidfilename,
        f_out.read(),
        content_type=OUTPUT_VIDEO_CONTENT_TYPE
    )

    # upload converted video to S3 and set the name.
    # save set to False to avoid infinite loop
    video.video_flv.save(
        vidfilename,
        suf,
        save=False
    )

    # delete temporary output file
    print "[convert_flv] removing temporary file: %s" % tmp_output_video
    os.remove(tmp_output_video)

    #video.flvfilename = vidfilename

    # add do_conversion=False to avoid infinite loop.
    # update_fields is needed in order to not delete video_thumbnail
    # if it did not exist when starting the task
    video.save(do_conversion=False, update_fields=['video_flv'])

@task
def ffmpeg_image(video_id):
    video = BroadcastUpload.objects.get(pk=video_id)
    print "ID: %s" %video.id
    id = video.id
    print "VIDEO NAME: %s" % video.video_upload.name
    teacher = video.teacher
    print "TEACHER: %s" % teacher
    filename = video.video_upload
    #sourcefile = "%s%s" % (settings.MEDIA_URL, filename)
    sourcefile = video.video_upload.url
    # ffmpeg cannot deal with https?
    sourcefile = sourcefile.replace("https","http")

    # temporary output image
    OUTPUT_IMAGE_EXT = 'png'
    OUTPUT_IMAGE_CONTENT_TYPE = 'image/png'
    f_out = tempfile.NamedTemporaryFile(suffix=".%s"%OUTPUT_IMAGE_EXT, delete=False)
    tmp_output_image = f_out.name

    #grabimage = "ffmpeg -y -i '%s' -vframes 1 -ss 00:00:02 -an -vcodec png -f rawvideo -s 320x240 '%s'" % (sourcefile, thumbnailfilename)
    grabimage = "ffmpeg -y -i '%s' -vframes 1 -ss 00:00:02 -an -vcodec png -f rawvideo -s 320x240 '%s'" % (sourcefile, tmp_output_image)
    print "ffmpeg_image: %s" % grabimage
    try:
         videothumbnail = subprocess.call(grabimage, shell=True)
         #also tried separately following line:
         #videothumbnail = commands.getoutput(grabimage)
         print "---------------IMAGE---------------"
         print "VIDEOTHUMBNAIL: %s" % videothumbnail
    except Exception as e:
         videothumbnail = None
         #print("Failed to extract thumbnail from %s to %s" % (sourcefile, thumbnailfilename))
         print("Failed to extract thumbnail from %s to %s" % (sourcefile, tmp_output_image))
         #print(traceback.format_exc())
         print "Error: %s" % e

    #imagefilename = "%s_%s.png" % (teacher, video.id)
    imagefilename = "%s_%s.%s" % (teacher, video.id, OUTPUT_IMAGE_EXT)
    #thumbnailfilename = "%svideos/flv/%s" % (settings.MEDIA_URL, thumbnailfilename)
    #thumbnailfilename = 'thumbnail_image.png'

    # prepare an object with the generated temporary image
    suf = SimpleUploadedFile(
        imagefilename,
        f_out.read(),
        content_type=OUTPUT_IMAGE_CONTENT_TYPE
    )

    # upload converted image to S3 and set the name.
    # save set to False to avoid infinite loop

    video.video_thumbnail.save(
        imagefilename,
        suf,
        save=False
    )

    # delete temporary output file
    print "[ffmpeg_image] removing temporary file: %s" % tmp_output_image
    os.remove(tmp_output_image)

    #video.videothumbnail = imagefilename

    # add do_conversion=False to avoid infinite loop
    video.save(do_conversion=False, update_fields=['video_thumbnail'])
