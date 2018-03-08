#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2018
# Gmail:liuzheng712
#


import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('jms_storage/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.md', 'rb') as f:
    readme = f.read().decode('utf-8')

with open('jms_storage.egg-info/requires.txt', 'r') as requirements_file:
    requirements = [x.strip() for x in requirements_file.readlines()]

setup(
    name='jms-storage',
    version=version,
    keywords=['jumpserver', 'storage', 'oss', 's3', 'aws'],
    description='Jumpserver storage python sdk tools',
    long_description=readme,
    license='MIT Licence',
    url='http://www.jumpserver.org/',
    author='Jumpserver team',
    author_email='liuzheng712@gmail.com',
    packages=['jms_storage'],
    include_package_data=True,
    install_requires=requirements,
    platforms='any',
)
