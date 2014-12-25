#!/usr/bin/env python

# stdlib
import os
import sys
from datetime import date

# not
import config

# evernote
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NoteStore


class NotClient(object):
    def __init__(self):
        client = EvernoteClient(token=config.TOKEN, Sandbox=False)
        self.store = client.get_note_store()
        self.notefilter = NoteStore.NoteFilter()

    def get_content(self, note_guid):
        note = self.store.getNote(note_guid, True, False, False, False)
        return note.content

    def search(self, title):
        try:
            # evernote's api is ridiculous
            self.notefilter.words = 'intitle:"{0}"'.format(title)
            note_guid = self.store.findNotesMetadata(self.notefilter,
                                                     0, 1,
                                                     NoteStore.NotesMetadataResultSpec()
                                                     ).notes[0].guid
            return note_guid
        except:
            return False

    def save(self, body, title):
        '''
        if the note exists, update it
        else, create it
        '''
        if self.search(title):
            note = self.store.getNote(self.note_guid, True, False, False, False)
            save_it = self.store.updateNote
        else:
            self.note = Types.Note()
            save_it = self.store.createNote

        note.title = title
        # evernotes special markup:
        note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>{0}</en-note>'.format(body)

        save_it(note)
