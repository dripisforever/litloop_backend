import boto3
import subprocess
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File
from pathlib import Path
from decouple import config
from .models import Lecture
from .utils import upload_to_s3

AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")

s3 = boto3.resource("s3")
bucket = s3.Bucket(AWS_STORAGE_BUCKET_NAME)


@receiver(post_save, sender=Lecture)
def handle_video_upload(sender, instance, created, **kwargs):

    file_relative_path = Path(instance.file.name)
    file_suffix = file_relative_path.suffix

    if not file_suffix == '.m3u8' and instance.file_type == "V":
        file_relative_dir = os.path.dirname(instance.file.name)

        file_relative_path_m3u8 = file_relative_path.with_suffix(".m3u8")
        file_name_m3u8 = file_relative_path_m3u8.name

        file_tmp_local_dir = f"/tmp/{file_relative_dir}"
        file_tmp_local_output = f"{file_tmp_local_dir}/{file_name_m3u8}"
        file_cloudfront_url = instance.file.url

        subprocess.run(['mkdir', '-p', file_tmp_local_dir])

        # ffmpeg_cmd = [
        #     "ffmpeg", "-i", file_cloudfront_url,
        #     "-f", "hls", file_tmp_local_output,
        #     "-loglevel", "quiet"
        # ]
        # subprocess.run(ffmpeg_cmd)

        subprocess.run([
            "ffmpeg", "-i", file_cloudfront_url,
            "-f", "hls", file_tmp_local_output,
            "-loglevel", "quiet"
        ])

        with open(file_tmp_local_output, "rb") as file_object:

            s3_file_dir = bucket.objects.filter(Prefix=file_relative_dir)
            s3_file_dir.delete()

            file_m3u8 = File(name=file_relative_path_m3u8, file=file_object)
            instance.file.save(file_name_m3u8, file_m3u8)

            ts_files = [
                x for x in Path(file_tmp_local_dir).iterdir()
                if str(x).endswith('.ts') is True
            ]

            for ts_file_path in ts_files:
                with open(ts_file_path, "rb") as ts_file_obj:
                    upload_to_s3(file_object=ts_file_obj,
                                 file_name=str(ts_file_path).replace(
                                     "/tmp/", ""))

            subprocess.run(["rm", "-r", file_tmp_local_dir])
