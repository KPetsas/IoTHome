#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Install the backend api packages. """
from setuptools import setup, find_packages
from api.__version__ import __version__

with open('requirements.txt') as f:
    requires = [line.rstrip('\n') for line in f]

setup(
    name='api',
    version=__version__,
    description='IoTHome application API.',
    author='Konstantinos Petsas',
    author_email='kons.petsas@gmail.com',
    packages=find_packages(exclude=('tests',)),
    install_requires=requires
)
