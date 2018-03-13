# -*- coding: utf-8 -*-
#
import boto3
import os

class aws:
    def __init__(self, config):
        self.BUCKET = config.get("BUCKET", "jumpserver")
        self.REGION = config.get("REGION", None)
        self.ACCESS_KEY = config.get("ACCESS_KEY", None)
        self.SECRET_KEY = config.get("SECRET_KEY", None)
        if self.ACCESS_KEY and self.REGION and self.SECRET_KEY:
            self.client = boto3.client('s3',
                                       region_name=self.REGION,
                                       aws_access_key_id=self.ACCESS_KEY,
                                       aws_secret_access_key=self.SECRET_KEY)
        else:
            self.client = boto3.client('s3')

    def type(self):
        return 's3'

    def upload_file(self, filepath, remote_path):
        try:
            self.client.upload_file(Filename=filepath, Bucket=self.BUCKET, Key=remote_path)
            return True
        except:
            return False

    def has_file(self, remote_path):
        try:
            self.client.head_object(Bucket=self.BUCKET, Key=remote_path)
            return True
        except:
            return False

    def download_file(self, remote_path, locale_path):
        try:
            os.makedirs(os.path.dirname(locale_path), 0o755)
            self.client.download_file(self.BUCKET, remote_path, locale_path)
            return True
        except:
            return False

    def delete_file(self, remote_path):
        try:
            self.client.delete_object(Bucket=self.BUCKET, Key=remote_path)
            return True
        except:
            return False

    def generate_presigned_url(self, path, expire=3600):
        try:
            return self.client.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': self.BUCKET, 'Key': path},
                ExpiresIn=expire,
                HttpMethod='GET')
        except:
            return False
