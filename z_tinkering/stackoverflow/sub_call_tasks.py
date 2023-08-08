# REFERENCE
import os, subprocess
from .models import Video

@app.task
def encode_mp4(video_id, height):
    try:
        video = Video.objects.get(id = video_id)
        input_file_path = video.original.path
        input_file_name = video.original.name

        #get the filename (without extension)
        filename = os.path.basename(input_file_path)

        # path to the new file, change it according to where you want to put it
        output_file_name = os.path.join('videos', 'mp4', '{}.mp4'.format(filename))
        output_file_path = os.path.join(settings.MEDIA_ROOT, output_file_name)

        # 2-pass encoding
        for i in range(1):
            subprocess.call([
                    settings.FFMPEG_PATH,
                    '-i', input_file_path,
                    '-s', '{}x{}'.format(height * 16 /9, height),
                    '-vcodec', 'mpeg4',
                    '-acodec', 'libvo_aacenc',
                    '-b', '10000k',
                    '-pass', i,
                    '-r', '30',
                    output_file_path
                ]
            )

        # Save the new file in the database
        video.mp4_720.name = output_file_name
        video.save(update_fields=['mp4_720'])
