# -*- coding: utf-8 -*-
#
import oss2
import os


class ali:
    def __init__(self, config):
        self.ENDPOINT = config.get("ENDPOINT", None)
        self.BUCKET = config.get("BUCKET", None)
        self.ACCESS_KEY = config.get("ACCESS_KEY", None)
        self.SECRET_KEY = config.get("SECRET_KEY", None)
        if self.ACCESS_KEY and self.SECRET_KEY:
            self.auth = oss2.Auth(self.ACCESS_KEY, self.SECRET_KEY)
        else:
            self.auth = None
        if self.auth and self.ENDPOINT and self.BUCKET:
            self.client = oss2.Bucket(self.auth, self.ENDPOINT, self.BUCKET)
        else:
            self.client = None

    def type(self):
        return 'oss'

    def upload_file(self, filepath, remote_path):
        try:
            self.client.put_object_from_file(remote_path, filepath)
            return True
        except:
            return False

    def has_file(self, remote_path):
        return self.client.object_exists(remote_path)

    def delete_file(self, remote_path):
        try:
            self.client.delete_object(remote_path)
            return True
        except:
            return False

    def download_file(self, remote_path, locale_path):
        try:
            os.makedirs(os.path.dirname(locale_path), 0o755)
            self.client.get_object_to_file(remote_path, locale_path)
            return True
        except:
            return False
