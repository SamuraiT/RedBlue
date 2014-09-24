#! /usr/bin/env python
# coding: utf-8
"""
Copyright 2014 Tatsuro Yasukawa.
"""

from distutils.core import setup
import os

def read_file(filename):
    filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), filename)
    if os.path.exists(filepath):
        return open(filepath).read()
    else:
        return ''

setup(
    name = 'RedBlue',
    packages = ['RedBlue'],
    version = '0.0.1',
    description = 'Event infomation extractor for Japanese events',
    author = "Tatsuro Yasukawa",
    author_email = "t.yasukawa01@gmail.com",
    maintainer = 'Tatsuro Yasukawa',
    maintainer_email = 't.yasukawa01@gmail.com',
    url = 'https://github.com/SamuraiT/RedBlue',
    license='new BSD',
    long_description = read_file('README.md'),
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Environment :: MacOS X",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)


