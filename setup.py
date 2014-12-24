#!/usr/bin/env python

from setuptools import setup

reqs = open('requirements.txt', 'r').readlines()

setup(name='not',
      author='Loren Carvalho',
      author_email='comradeloren[at]gmail.com',
      url='http://hullcrushdepth.com',
      version='0.0.4',
      packages=['notpy'],
      install_requires=reqs,

      entry_points={
          'console_script': [
              'not = notpy.cmd:cli',
              'not-setup = notpy.cmd:setup'
              ]
          }
      )
