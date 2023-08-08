# ref https://stackoverflow.com/questions/70183051/how-to-download-new-uploaded-files-from-s3-to-ec2-everytime
import boto3

def upload_folder(src_directory, target_s3_directory):
    s3 = boto3.client('s3')
    for root, dirs, files in os.walk(src_directory):
        for filename in files:
            local_path = os.path.join(root, filename)

            relative_path = os.path.relpath(local_path, src_directory)
            s3_path = os.path.join(target_s3_directory, relative_path)
            
            # boto upload
            s3.upload_file(local_path, TRANSCODE_BUCKET_NAME, s3_path)


def main() -> None:
    s3 = boto3.client('s3')
    sqs = boto3.client('sqs')
    while True:
        res = sqs.receive_message(QueueUrl="yourQueue", WaitTimeSeconds=20,)

        for msg in res.get("Messages", []):
            s3.download_file("yourBucket", msg["key"], "local/file/path")

            to_hls.delay() # ffmpeg
            upload_transcoded_to_s3.delay() #

            # ref https://luis-sena.medium.com/build-an-auto-scaling-transcoding-platform-using-python-ffmpeg-aws-950645fe5e07
            # upload_folder(HLS_PATH, HLS_PATH)
