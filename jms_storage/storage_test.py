#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2018
# Gmail:liuzheng712
#

import sys
import os
import unittest

sys.path.append('..')
import jms_storage
import config


class TestStorageFunc(unittest.TestCase):
    file_tmp_path = '/tmp/README.md'
    file_locale_path = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir, 'README.md'))
    file_remote_path = 'README.md'

    def test_upload_file(self):
        self.assertTrue(self.client.delete_file(self.file_remote_path))
        self.assertTrue(self.client.upload_file(self.file_locale_path, self.file_remote_path))

    def test_download_file(self):
        if os.path.isfile(self.file_tmp_path):
            os.remove(self.file_tmp_path)
        self.assertTrue(self.client.download_file(self.file_remote_path, self.file_tmp_path))

    def test_generate_presigned_url(self):
        # print(self.client.generate_presigned_url(self.file_remote_path))
        pass


class TestAWS(TestStorageFunc):
    client = jms_storage.S3Storage(config.aws_config)

    def test_type(self):
        self.assertEqual(self.client.type(), 's3')


class TestAli(TestStorageFunc):
    client = jms_storage.OSSStorage(config.ali_config)

    def test_type(self):
        self.assertEqual(self.client.type(), 'oss')


def suite():
    suite = unittest.TestSuite()
    test_cases = ['test_type',
                  'test_upload_file',
                  'test_download_file',
                  'test_generate_presigned_url',
                  ]

    for test_class in test_cases:
        suite.addTest(TestAWS(test_class))
        suite.addTest(TestAli(test_class))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
