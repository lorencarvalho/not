"""
constants
override via environment variables
"""

import os


SUFFIX = os.environ.get('NOT_SUFFIX', '.md')
EDITOR = os.environ.get('EDITOR', 'vim')
TOKENPATH = os.environ.get('NOT_TOKEN', os.path.join(os.environ['HOME'], '.not_token'))
DEFAULT_LOGLEVEL = os.environ.get('NOT_LOGLEVEL', 'WARN')

# for evernote api
CONSUMER_KEY = 'comradeloren'
CONSUMER_SECRET = 'c219754d19198564'
