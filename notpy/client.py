"""
provides NotClient, the subclassed evernote client
"""
from __future__ import with_statement

import logging
import os
import tempfile

import evernote.edam.type.ttypes as Types
import markdown2

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from evernote.edam.type.ttypes import NoteSortOrder

from .enml import enml_to_text

log = logging.getLogger(__name__)


class NoteSaveError(Exception):
    def __init__(self, exc, note_contents=''):
        """ return a cleanly formatted exception & save the unsaved note to a tempfile. """
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(note_contents)
            name = f.name
        message = "{0}\nUnsaved note saved to {1}".format(exc, name)
        super(NoteSaveError, self).__init__(message)


class NotNote(object):
    """ this class provides the evernote special markup to our plaintext/md notes. """
    def __init__(self, body):
        self.body = markdown2.markdown(body)

    def __str__(self):
        note_string = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
            '<en-note>'
            '{body}'
            '</en-note>'.format(body=self.body)
        )
        return note_string

    def __repr__(self):
        return self.__str__()


class NotClient(EvernoteClient):
    def __init__(self, *args, **kwargs):
        """ subclass evernote client and get a note store obj """
        super(NotClient, self).__init__(*args, **kwargs)
        self.store = self.get_note_store()

    def get_content(self, note_guid):
        """ get the actual contents of a note based on guid """
        note = self.store.getNote(note_guid, True, False, False, False)
        # Strip html/xml tags
        content = enml_to_text(note.content)
        log.debug("Got text content from note guid {0}: {1}".format(note_guid, note.content))
        return content

    def get_title(self, note_guid):
        note = self.store.getNote(note_guid, True, False, False, False)
        return note.title

    def search(self, title=None, max_results=1):
        """ bumble through evernote's weird api to find a note. """
        if title:
            title = "intitle:'{title}'".format(title=title)

        notefilter = NoteFilter(order=NoteSortOrder.UPDATED, words=title)
        finder = self.store.findNotesMetadata(notefilter, 0, max_results, NotesMetadataResultSpec())
        notes = finder.notes
        if notes:
            return [note.guid for note in finder.notes]

    def get_tags(self, body):
        """ search the note for 'tags: tag1, tag2' """
        for line in body.splitlines():
            if line.startswith('tags:'):
                return [tag.strip() for tag in line.partition(':')[2].split(',')]

    def save(self, body, title):
        """ if the note exists, update it otherwise create it. """
        try:
            note_guid = self.search(title)
            if note_guid:
                note_obj = self.store.getNote(note_guid[0], True, False, False, False)
                save_method = self.store.updateNote
            else:
                note_obj = Types.Note()
                save_method = self.store.createNote

            # look for and attach tags:
            note_obj.tagNames = self.get_tags(body)

            # set title
            note_obj.title = title

            # populate content w/evernote special markup
            note_obj.content = str(NotNote(body))

            # save new note or update existing
            save_method(note_obj)
        except Exception as e:
            raise NoteSaveError(e, body)
