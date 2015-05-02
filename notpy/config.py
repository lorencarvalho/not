#!/usr/bin/env python
'''
this constantsy file is for configuring stuff
more than likely you won't edit it
'''

import os


try:
    token = open(os.path.join(os.environ['HOME'], '.not_token')).read()
except Exception as e:
    print 'No token! run not-setup! {0}'.format(e)


SUFFIX = '.md'
EDITOR = os.environ.get('EDITOR', 'vim')
TOKEN = token
CONSUMER_KEY = 'comradeloren'
CONSUMER_SECRET = 'c219754d19198564'
DEFAULT_LOGLEVEL = 'WARN'
