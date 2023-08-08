
# AWS_REGION = os.environ['AWS_REGION']
# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

AWS_REGION = os.environ.get('AWS_REGION')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_S3_USE_SSL = os.environ.get('AWS_S3_USE_SSL', 'false').lower() == 'true'
AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')
AWS_QUERYSTRING_AUTH = False
IMAGEKIT_CACHE_TIMEOUT = None
# Default bucket settings

# AWS_STORAGE_BUCKET_NAME = os.environ['BUCKET_STATIC']
AWS_STORAGE_BUCKET_NAME = os.environ.get('BUCKET_STATIC') #comment

AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')

# BUCKET_MEDIA = os.environ['BUCKET_MEDIA']
BUCKET_MEDIA = os.environ.get('BUCKET_MEDIA') #comment

# CLOUDFRONT
AWS_CLOUDFRONT_DOMAIN = 'https://xxxxx.cloudfront.net'
CLOUDFRONT_MEDIA_URL = 'https://{media-distribution-id}.cloudfront.net/'

S3_NETWORK_TIMEOUT = 10000
S3_NETWORK_RETRY_COUNT = 32
AWS_DEFAULT_ACL = 'public-read'
# Media bucket settings
BUCKET_MEDIA_CUSTOM_DOMAIN = os.environ.get('BUCKET_MEDIA_CUSTOM_DOMAIN')
BUCKET_MEDIA_DEFAULT_ACL = None
BUCKET_STATIC_CUSTOM_DOMAIN = os.environ.get('BUCKET_STATIC_CUSTOM_DOMAIN')

# DEFAULT_FILE_STORAGE = 'media.custom_storage.CustomS3Boto3Storage'
# STATICFILES_STORAGE = os.environ.get(
#     'STATICFILES_STORAGE', DEFAULT_FILE_STORAGE
# )
