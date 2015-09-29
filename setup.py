#!/usr/bin/env python

from setuptools import setup


reqs = ['evernote', #==1.24',
        'argparse']


entry_points = {'console_scripts': [
                'not = notpy.cmd:cli',
                'not-setup = notpy.oauth:setup']}


setup(name='not',
      author='Loren Carvalho',
      author_email='comradeloren[at]gmail.com',
      description='note without the e(vernote), the quickest dirtiest cli evernote client ever',
      url='http://hullcrushdepth.com',
      license='MIT',
      version='1.0.1',
      packages=['notpy'],
      install_requires=reqs,
      entry_points=entry_points,
      )
