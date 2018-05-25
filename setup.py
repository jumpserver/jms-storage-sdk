#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2018
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

with open('requirements.txt', 'r') as f:
    requirements = [x.strip() for x in f.readlines()]

setup(
    name='jms-storage',
    version=version,
    keywords=['jumpserver', 'storage', 'oss', 's3', 'elasticsearch'],
    description='Jumpserver storage python sdk tools',
    long_description=readme,
    license='MIT Licence',
    url='http://www.jumpserver.org/',
    author='Jumpserver team',
    author_email='support@fit2cloud.com',
    packages=['jms_storage'],
    data_files=[('requirements', ['requirements.txt'])],
    include_package_data=True,
    install_requires=requirements,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
