# ref https://github.com/metr1ckzu/youtube-mp3-download/blob/12cb1562f811a61be4793ba13dceb35f855334eb/downloader/tasks.py

from __future__ import absolute_import

import os
import shutil
import subprocess
import uuid

from django.conf import settings

from celery import shared_task, Celery

from downloader.models import Video
from downloader.utils import create_filename, get_video_info

@shared_task
def convert(url):
    result = None
    duration = None

    info = get_video_info(url)
    if info: duration = info.get('duration')

    if info and duration and duration <= settings.MAX_DURATION_SECONDS:
        youtube_id = info['id']
        title = info['title']

        audio_filename = create_filename(info['title'])

        video, created = Video.objects.get_or_create(youtube_id=youtube_id)
        video.url = url
        video.save()

        result = {
            'youtube_id': youtube_id,
            'title': title
        }

        output_filepath = os.path.join(settings.MEDIA_ROOT, audio_filename)
        if os.path.exists(output_filepath):
            result['filename'] = audio_filename
        else:
            conversion_result = start_conversion(url, audio_filename, video)

            if conversion_result == 0:
                result['filename'] = audio_filename
    return result

def start_conversion(url, audio_filename, video):
    temp_filepath = os.path.join(settings.MEDIA_ROOT, '{0}_{1}'.format(uuid.uuid4(), audio_filename))
    output_filepath = os.path.join(settings.MEDIA_ROOT, audio_filename)

    result = subprocess.check_call([
        'youtube-dl',
        '--no-playlist',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--output', temp_filepath,
        '--cache-dir', '/tmp/youtube_dl',
        url,
    ])

    if result == 0:
        shutil.move(temp_filepath, output_filepath)

        video.audio_filename = audio_filename
        video.save()

    return result
