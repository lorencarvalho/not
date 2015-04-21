#!/usr/bin/env python

import os
import subprocess
from setuptools import setup, Command

reqs = open('requirements.txt', 'r').readlines()

entry_points = {
          'console_scripts': [
              'not = notpy.cmd:cli',
              'not-setup = notpy.oauth:setup'
              ]
          }


class Pex(Command):
  user_options = []

  def initialize_options(self):
    """Abstract method that is required to be overwritten"""

  def finalize_options(self):
    """Abstract method that is required to be overwritten"""

  def run(self):
    if not os.path.exists('dist/wheel-cache'):
      print('You need to create dist/wheel-cache first! You\'ll need to run the following.')
      print('  mkdir dist/wheel-cache')
      print('  pip wheel -w dist/wheel-cache')
      return
    for entry in entry_points['console_scripts']:
      name, call = tuple([_.strip() for _ in entry.split('=')])
      print('Creating {0} as {1}'.format(name, call))
      subprocess.check_call([
        'pex',
        '-r', 'not',
        '--no-pypi',
        '--repo=dist/wheel-cache',
        '-o', name,
        '-e', call])


setup(name='not',
      author='Loren Carvalho',
      author_email='comradeloren[at]gmail.com',
      url='http://hullcrushdepth.com',
      version='1.0',
      packages=['notpy'],
      install_requires=reqs,
      cmdclass={'pexify': Pex},
      entry_points=entry_points,
      )
