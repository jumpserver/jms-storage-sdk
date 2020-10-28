# -*- coding: utf-8 -*-
#

import os
from ftplib import FTP
from .base import ObjectStorage


class FTPStorage(ObjectStorage):

    def __init__(self, config):
        self.host = config.get("HOST", None)
        self.port = config.get("PORT", 21)
        self.username = config.get("USERNAME", None)
        self.password = config.get("PASSWORD", None)
        self.client = FTP()
        self.client.encoding = 'utf-8'
        self.client.set_pasv(True)
        self.connect()

    def connect(self, timeout=-999, source_address=None):
        self.client.connect(self.host, self.port, timeout, source_address)
        self.client.login(self.username, self.password)

    def upload(self, src, target):
        file_name = target.rsplit('/', 1)[-1] if '/' in target else target
        if self.exists(target):
            raise Exception('File exist error(%s)' % target)
        try:
            with open(src, 'rb') as f:
                self.client.storbinary('STOR '+file_name, f)
            return True, None
        except Exception as e:
            return False, e
        finally:
            self.client.close()

    def download(self, src, target):
        try:
            os.makedirs(os.path.dirname(target), 0o755, exist_ok=True)
            with open(target, 'wb') as f:
                self.client.retrbinary('RETR ' + src, f.write)
            return True, None
        except Exception as e:
            return False, e
        finally:
            self.client.close()

    def delete(self, path):
        file_name = path.rsplit('/', 1)[-1] if '/' in path else path
        if not self.exists(path):
            raise Exception('File not exist error(%s)' % path)
        try:
            self.client.delete(file_name)
            return True, None
        except Exception as e:
            return False, e

    def exists(self, path):
        if '/' in path:
            remote_dir, file_name = path.rsplit('/', 1)[0], path.rsplit('/', 1)[1]
        else:
            remote_dir, file_name = '/', path
        try:
            self.client.cwd(remote_dir)
            if file_name in self.client.nlst():
                return True
            return False
        except:
            self.client.mkd(remote_dir)
            self.client.cwd(remote_dir)
            return False
