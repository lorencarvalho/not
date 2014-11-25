#!/usr/bin/env python

from setuptools import setup

reqs = open('requirements.txt', 'r').readlines()

setup(name='not',
      author='Loren Carvalho',
      author_email='comradeloren[at]gmail.com',
      url='http://hullcrushdepth.com',
      version='0.0.2',
      packages=['notpy', 'evernote'],
      scripts=['not'],
      install_requires=reqs
      )
