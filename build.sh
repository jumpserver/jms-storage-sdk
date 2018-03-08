#!/bin/bash
# coding: utf-8
# Copyright (c) 2018
# Gmail: liuzheng712
#

set -ex

python setup.py sdist && \
twine upload dist/*.tar.gz
