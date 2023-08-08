# views.py

from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from .models import Video

class ChunkedUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, format=None):
        file_obj = request.data['file']
        video = Video.objects.create(video_file=file_obj)
        return Response({'video_id': video.id}, status=status.HTTP_201_CREATED)
