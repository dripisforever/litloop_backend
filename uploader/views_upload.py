# ref https://github.com/ritlew/django-hls-video/

from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView

# from drf_chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView


class VideoChunkedUploadView(ChunkedUploadView):
    model = VideoChunkedUpload
    field_name = 'raw_video_file'

    def check_permissions(self, request):
        return request.user.is_superuser or request.user.is_staff


class VideoChunkedUploadCompleteView(ChunkedUploadCompleteView):
    model = VideoChunkedUpload
    do_md5_check = False

    def check_permissions(self, request):
        return request.user.is_superuser or request.user.is_staff

    def on_completion(self, uploaded_file, request):
        vid, created = Video.objects.get_or_create(user=request.user, upload_id=request.POST.get("upload_id"))

        vid.begin_processing()

        return JsonResponse({})


    def get_response_data(self, chunked_upload, request):
        return {
            'message': ("You successfully uploaded '%s' (%s bytes)!" % (chunked_upload.filename, chunked_upload.offset))
        }
