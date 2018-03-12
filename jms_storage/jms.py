# -*- coding: utf-8 -*-
#
import os


class jms:
    def __init__(self, service):
        self.client = service

    def type(self):
        return 'jms'

    def upload_file(self, filepath, remote_path):
        try:
            self.client.push_session_replay(filepath, os.path.basename(filepath).split('.')[0])
            return True
        except:
            return False

    def has_file(self, remote_path):
        return self.client.object_exists(remote_path)

    def download_file(self, remote_path, locale_path):
        try:
            self.client.get_object_to_file(remote_path, locale_path)
            return True
        except:
            return False
