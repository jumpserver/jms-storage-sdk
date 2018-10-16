# -*- coding: utf-8 -*-
#

import os

from azure.storage.blob import BlockBlobService

from .base import ObjectStorage


class AzureStorage(ObjectStorage):

    def __init__(self, config):
        self.account_name = config.get("ACCOUNT_NAME", None)
        self.account_key = config.get("ACCOUNT_KEY", None)
        self.container_name = config.get("CONTAINER_NAME", None)
        self.endpoint_suffix = config.get("ENDPOINT_SUFFIX", 'core.chinacloudapi.cn')

        if self.account_name and self.account_key:
            self.client = BlockBlobService(
                account_name=self.account_name, account_key=self.account_key,
                endpoint_suffix=self.endpoint_suffix
            )
        else:
            self.client = None

    def upload(self, src, target):
        try:
            self.client.create_blob_from_path(self.container_name, target, src)
            return True, None
        except Exception as e:
            return False, e

    def download(self, src, target):
        try:
            os.makedirs(os.path.dirname(target), 0o755, exist_ok=True)
            self.client.get_blob_to_path(self.container_name, src, target)
            return True, None
        except Exception as e:
            return False, e

    def delete(self, path):
        try:
            self.client.delete_blob(self.container_name, path)
            return True, False
        except Exception as e:
            return False, e

    def exists(self, path):
        return self.client.exists(self.container_name, path)

    @property
    def type(self):
        return 'azure'
