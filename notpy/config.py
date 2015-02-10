#!/usr/bin/env python

import os

def token():
    try:
        return open(os.path.join(os.environ['HOME'], '.not_token')).read()
    except Exception as e:
        return 'No token! run not-setup! {0}'.format(e)

EDITOR = os.environ.get('EDITOR', 'vim')
TOKEN = token()
CONSUMER_KEY = 'comradeloren'

# ok, so, evernote doesn't have any resources on whether or not this 
# "secret" should remain a secret, and other evernote apps on github
# have this in their revision control, best I can tell you have to have it
# in order to instantiate the oauth client and whatnot. fuck it.
CONSUMER_SECRET = 'c219754d19198564'
