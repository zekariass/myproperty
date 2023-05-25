from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticFileStorage(S3Boto3Storage):
    location = settings.STATICFILE_FOLDER


class MediaFileStorage(S3Boto3Storage):
    location = settings.MEDIAFILE_FOLDER