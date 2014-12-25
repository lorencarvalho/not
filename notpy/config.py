#!/usr/bin/env python

import os

def token():
    try:
        return open(os.path.join(os.environ['HOME'], '.not_token')).read()
        print 'GET DAT TOKEN'
        print open(os.path.join(os.environ['HOME'], '.not_token')).read()
    except Exception as e:
        return 'No token! run not-setup! {0}'.format(e)

EDITOR = os.environ.get('EDITOR', 'vim')
TOKEN = token()
USER_BASE_URL = "www.evernote.com"
CONSUMER_KEY = 'comradeloren'
CONSUMER_SECRET = 'c219754d19198564'
