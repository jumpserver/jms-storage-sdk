#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2018
# Gmail:liuzheng712
#

__version__ = '0.0.13'

from .ali import ali
from .aws import aws
from .jms import jms
from .es import ESStore


def init(config):
    if config['TYPE'] == 's3':
        return aws(config)
    elif config['TYPE'] == 'oss':
        return ali(config)
    else:
        return None
