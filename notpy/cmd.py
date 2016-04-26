"""
command module for Not
provides the `not` executable
"""

import argparse
import hashlib
import tempfile
import sys
import logging

from datetime import date
from functools32 import lru_cache
from subprocess import call

from . import client, constants

log = logging.getLogger(__name__)


@lru_cache(maxsize=12)
def get_client():
    try:
        with open(constants.TOKENPATH) as token_fh:
            token = token_fh.read()
            return client.NotClient(token=token, sandbox=False)
    except Exception:
        log.critical("Unable to setup NotClient\nYou may need to run `not-setup` and try again")
        sys.exit(1)


def md5sum(f):
    """ simply returns an md5sum of the contents of your note """
    with open(f) as fh:
        md5 = hashlib.md5(fh.read()).hexdigest()
    return md5


def cli():
    """ opens or creates the note, uses today's date or an explicit title """
    parser = argparse.ArgumentParser(description='not')
    parser.add_argument('title', nargs='?', default=str(date.today()))
    parser.add_argument('-l', '--loglevel', default=constants.DEFAULT_LOGLEVEL, help=argparse.SUPPRESS)
    args = vars(parser.parse_args())

    # Do setup stuff
    log.setLevel(args['loglevel'])
    title = args['title']
    not_client = get_client()

    # really inelegant arg parsing
    if title == 'ls':
        note_guids = not_client.search(max_results=10)
        notes = [not_client.get_title(guid) for guid in note_guids]
        print("10 most recently edited notes:")
        for bullet in [" * {note}".format(note=note) for note in notes]:
            print(bullet)
        sys.exit(0)

    def try_first_result(result, title):
        try:
            return result[0]
        except IndexError:
            log.debug('No note found for title: %s', title)
            return None

    if sys.stdin.isatty():
        # Nothing is being piped in, so open a file and let the user edit it
        with tempfile.NamedTemporaryFile(suffix=constants.SUFFIX) as f:
            log.debug("Created temp file at {name}".format(name=f.name))
            note_id = try_first_result(not_client.search(title), title)
            if note_id:
                content = not_client.get_content(note_id)
                log.debug("Got content: {0}".format(content))
                f.write(content)
                f.flush()

            md5 = md5sum(f.name)
            call([constants.EDITOR, '+', f.name])
            if md5sum(f.name) != md5:
                content = open(f.name).read().strip()
                not_client.save(content, title)

    else:
        # The user is trying to pipe things in through stdin
        note_id = try_first_result(not_client.search(title), title)
        if note_id:
            content = not_client.get_content(existing_note_guid)
        else:
            content = ''

        content += '\n'.join(line for line in sys.stdin)

        not_client.save(content, title)
