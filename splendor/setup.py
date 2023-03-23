#!/usr/bin/env python
from setuptools import setup

setup(
    name='splendor',
    description='splendor core code',
    packages=[
    ],
    install_requires=[
        'py_cui',
        'termcolor',
        'dotted-dict',
        'lmdb',
        'keras',
        'tensorflow'
    ],
    dependency_links=[
    ],
    extras_require={
        'dev': [
        ]
    }
)
