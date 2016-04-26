#!/usr/bin/env python

from setuptools import setup


reqs = [
    'evernote',  # ==1.24',
    'bs4',
    'html2text',
    'markdown2',
    'functools32',
    'argparse'
]

entry_points = {
    'console_scripts': [
        'not = notpy.cmd:cli',
        'not-setup = notpy.oauth:setup',
    ]
}

setup(name='not',
      author='Loren Carvalho',
      author_email='me@loren.pizza',
      description='note without the e(vernote), the quickest dirtiest cli evernote client ever',
      url='https://loren.pizza',
      license='MIT',
      version='2.0.2',
      packages=['notpy'],
      install_requires=reqs,
      entry_points=entry_points,
      )
