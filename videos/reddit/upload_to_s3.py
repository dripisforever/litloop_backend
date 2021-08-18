import logging
import boto3
from decouple import config
from botocore.exceptions import ClientError

AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")


def upload_to_s3(file_object, file_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    s3_client = boto3.client('s3')
    try:
        s3_client.upload_fileobj(Fileobj=file_object,
                                 Bucket=AWS_STORAGE_BUCKET_NAME,
                                 Key=file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
