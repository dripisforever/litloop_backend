# tasks.py

import os
from celery import shared_task
import ffmpeg

@shared_task
def transcode_to_hls(video_id):
    from your_app.models import Video, Encoding, EncodeProfile
    video = Video.objects.get(id=video_id)
    video_path = video.video_file.path
    hls_output_dir = os.path.dirname(video.hls_file.path)
    os.makedirs(hls_output_dir, exist_ok=True)

    encoding_profiles = EncodeProfile.objects.all()

    for profile in encoding_profiles:
        output_path = os.path.join(hls_output_dir, f'{profile.resolution}_{video.id}.m3u8')

        (
            ffmpeg
            .input(video_path)
            .output(output_path, vf=f'scale={profile.resolution}', b=profile.bitrate, f='hls', hls_time=10, hls_list_size=0)
            .run()
        )

        Encoding.objects.create(video=video, encoding_profile=profile, is_complete=True)
