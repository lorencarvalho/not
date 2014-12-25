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
from notpy import NotClient, config

try:
    not_client = NotClient()
except Exception as e:
    print "need to run not-setup"
    print e
    import sys; sys.exit(1)


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
    note = not_client.search(title)
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
            not_clien.save(open(f.name).read(), title=args['title'])
