#!/usr/bin/env python
'''
command module for Not
provides the `not` executable
'''
import argparse
import hashlib
import tempfile
import sys
import logging
from datetime import date
from subprocess import call
from notpy import NotClient, config, NoteSaveError

logger = None


def setup_logging(l):
    try:
        level = getattr(logging, l.upper())
    except AttributeError:
        level = getattr(logging, config.DEFAULT_LOGLEVEL)

    logging.basicConfig(level=level)
    global logger
    logger = logging.getLogger(__name__)
    logger.debug("Successfully set up logger at {0} level".format(logging.getLevelName(level)))


def setup_client():
    try:
        token = open(config.TOKENPATH).read()
        global not_client
        not_client = NotClient(token=token, sandbox=False)
    except:
        logger.critical("Unable to setup NotClient\nYou may need to run `not-setup` and try again")
        logger.debug("Path to token file: %s", config.TOKENPATH
        logger.debug("Contents of token file: %s", token)
        sys.exit(1)


def md5sum(f):
    '''
    simply returns an md5sum of the contents of your note
    '''
    return hashlib.md5(open(f).read()).hexdigest()


def save_with_retry(content, title):
    '''
    if you leave your editor open for a while sometimes you
    have to reinstantiate your client

    I can't reproduce this reliabily, so idk if this even works - lol
    '''
    for attempt in range(0, 2):
        try:
            not_client.save(content, title=title)
        except NoteSaveError:
            not_client = setup_client()


def cli():
    '''
    opens or creates the note, uses today's date or an explicit title
    '''
    parser = argparse.ArgumentParser(description='not')
    parser.add_argument('title', nargs='?', default=str(date.today()))
    parser.add_argument('-l', '--loglevel', default=config.DEFAULT_LOGLEVEL, help=argparse.SUPPRESS)
    args = vars(parser.parse_args())

    # Do setup stuff
    setup_logging(args['loglevel'])
    setup_client()
    title = args['title']

    if title == 'ls':
        notes = not_client.search(ls=True)
        print '\n'.join([not_client.get_title(guid) for guid in notes])
        sys.exit(0)

    if sys.stdin.isatty():
        # Nothing is being piped in, so open a file and let the user edit it
        with tempfile.NamedTemporaryFile(suffix=config.SUFFIX) as f:
            logger.debug("Created temp file at {0}".format(f.name))
            note_id = not_client.search(title)
            logger.debug("Note ID found: {0}".format(note_id))
            if note_id:
                content = not_client.get_content(note_id)
                logger.debug("Got content: {0}".format(content))
                f.write(content)
                f.flush()

            md5 = md5sum(f.name)
            call([config.EDITOR, '+', f.name])
            if md5sum(f.name) != md5:
                content = open(f.name).read().strip()
                save_with_retry(content, title)

    else:
        # The user is trying to pipe things in through stdin
        existing_note_guid = not_client.search(title)
        if existing_note_guid:
            content = not_client.get_content(existing_note_guid)
        else:
            content = ''

        content += '\n'.join(line for line in sys.stdin)

        save_with_retry(content, title)
