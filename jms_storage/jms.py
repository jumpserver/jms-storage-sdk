# -*- coding: utf-8 -*-
#
import os
from .base import ObjectStorage


class JMSReplayStorage(ObjectStorage):
    def __init__(self, service):
        self.client = service

    def upload(self, src, target):
        session_id = os.path.basename(target).split('.')[0]
        ok = self.client.push_session_replay(src, session_id)
        return ok, None

    def delete(self, path):
        pass

    def exists(self, path):
        pass

    def download(self, src, target):
        pass

    @property
    def type(self):
        return 'jms'
