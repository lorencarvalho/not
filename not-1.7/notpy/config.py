#!/usr/bin/env python
'''
this constantsy file is for configuring stuff
more than likely you won't edit it
'''

import os


SUFFIX = '.md'
EDITOR = os.environ.get('EDITOR', 'vim')
TOKENPATH = os.path.join(os.environ['HOME'], '.not_token')
CONSUMER_KEY = 'comradeloren'
CONSUMER_SECRET = 'c219754d19198564'
DEFAULT_LOGLEVEL = 'WARN'
