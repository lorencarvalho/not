#!/usr/bin/env python

from setuptools import setup

reqs = open('requirements.txt', 'r').readlines()


entry_points = {'console_scripts': [
                'not = notpy.cmd:cli',
                'not-setup = notpy.oauth:setup']}


setup(name='not',
      author='Loren Carvalho',
      author_email='comradeloren[at]gmail.com',
      url='http://hullcrushdepth.com',
      version='1.0',
      packages=['notpy'],
      install_requires=reqs,
      entry_points=entry_points,
      )
