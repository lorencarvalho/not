#!/usr/bin/env python
'''
command module for Not
hint: 'f' always refers to the temp file
      'n' is the evernote api wrapper "notpy.Note()"
'''
import argparse
import hashlib
import tempfile
import re
from datetime import date
from subprocess import call
from notpy import Note, config

authtoken = config.TOKEN
n = Note(authtoken)


def md5sum(f):
    '''
    simply returns an md5sum of the contents of your note
    '''
    return hashlib.md5(open(f).read()).hexdigest()


def check_existing(title, f):
    '''
    checks if your note already exists based on title
    if it does, grabs the contents so we can append
    '''
    note = n.search(title)
    if note:
        content = re.sub('<br/>', '\n',n.get_content(note))
        content = re.sub('<.*?>', '', content)
        open(f, 'w').write(content)
    return f


def cli():
    '''
    opens or creates the note, uses today's date or an explicit title
    '''
    parser = argparse.ArgumentParser(description='not')
    parser.add_argument('title', nargs='?', default=str(date.today()))
    args = vars(parser.parse_args())

    with tempfile.NamedTemporaryFile() as f:
        check_existing(args['title'], f.name)
        md5 = md5sum(f.name)
        call([config.EDITOR, f])
        if md5sum(f.name) != md5:
            n.save(open(f.name).read(), title=args['title'])


def setup():
    '''
    oauth flow for new users or updating users
    most of this was shamelessly copied from :
    https://gist.github.com/inkedmn/5041037
    '''
    from evernote.api.client import EvernoteClient

    def parse_query_string(authorize_url):
        uargs = authorize_url.split('?')
        vals = {}
        if len(uargs) == 1:
            raise Exception('Invalid Authorization URL')
        for pair in uargs[1].split('&'):
            key, value = pair.split('=', 1)
            vals[key] = value
        return vals

    consumer_key = config.CONSUMER_KEY
    consumer_secret = config.CONSUMER_SECRET
    request_token = client.get_request_token('http://localhost')
    print "Paste this URL in your browser and login"
    print '\t'+client.get_authorize_url(request_token)
    print "Paste the URL you get after logging in here:" 
    authurl = raw_input()
    vals = parse_query_string(authurl)
    auth_token = client.get_access_token(
                 request_token['oauth_token'],
                 request_token['oauth_token_secret'],
                 vals['oauth_verifier']
                )
    with open(os.path.join(os.environ.get['HOME'], '.not_token')) as f:
        f.write(auth_token)
    
