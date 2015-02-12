#!/usr/bin/env python
'''
command module for Not
provides the `not` executable
hint: 'f' always refers to the temp file
      'n' is the evernote api wrapper "notpy.Note()"
'''
import argparse
import hashlib
import tempfile
import re
import sys
from datetime import date
from subprocess import call
from notpy import NotClient, config

try:
    not_client = NotClient(token=config.TOKEN, sandbox=False)
except:
    print "bailing!"
    print "you may need to run `not-setup` and try again"
    sys.exit(1)


def md5sum(f):
    '''
    simply returns an md5sum of the contents of your note
    '''
    return hashlib.md5(open(f).read()).hexdigest()


def format_to_plain_text(content):
    '''
    Given the contents of an existing note, strip out all the HTML tags
    '''
    content = re.sub('<br/>', '\n', content)
    content = re.sub('<.*?>', '', content)
    return content


def check_existing(title, f):
    '''
    checks if your note already exists based on title
    if it does, grabs the contents so we can append
    '''
    note = not_client.search(title)
    if note:
        content = format_to_plain_text(not_client.get_content(note))
        open(f, 'w').write(content)
    return f


def note_save_error(e, guts):
    print 'failed to save note!\n\n'
    print 'exception was: {0}\n\n'.format(e)
    print 'contents of unsaved note: \n\n'
    print guts


def cli():
    '''
    opens or creates the note, uses today's date or an explicit title
    '''
    parser = argparse.ArgumentParser(description='not')
    parser.add_argument('title', nargs='?', default=str(date.today()))
    args = vars(parser.parse_args())

    if sys.stdin.isatty():
        # Nothing is being piped in, so open a file and let the user edit it
        with tempfile.NamedTemporaryFile(suffix=config.SUFFIX) as f:
            check_existing(args['title'], f.name)
            md5 = md5sum(f.name)
            call([config.EDITOR, '+', f.name])
            if md5sum(f.name) != md5:
                guts = open(f.name).read().strip()
                try:
                    not_client.save(guts, title=args['title'])
                except Exception as e:
                    note_save_error(e, guts)
    else:
        # The user is trying to pipe things in through stdin
        existing_note_guid = not_client.search(args['title'])
        if existing_note_guid:
            content = format_to_plain_text(
                not_client.get_content(existing_note_guid))
        else:
            content = ''

        content += '\n'.join(line for line in sys.stdin)

        try:
            not_client.save(content, title=args['title'])
        except Exception as e:
            note_save_error(e, content)
