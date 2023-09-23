from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    bucket_name = 'my-media-bucket'

# AWS_S3_OBJECT_PARAMETERS = {
#     'Expires': '',
#     'CacheControl': 'max-age=94608000',
# }

AWS_STORAGE_BUCKET_NAME = 'studio-media'
AWS_S3_REGION_NAME = 'us-east-2'  # e.g. us-east-2
#AWS_ACCESS_KEY_ID = 'AKIA4BCPEYX3WHIK3XVE'
#AWS_SECRET_ACCESS_KEY = 'jOYCg2ZiDB/+GDiOuPBE55I7bpwOi2NjJkJn9Od7'

# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# Application definition

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'




