#!/usr/bin/env python

# stdlib
import os
import sys
from datetime import date

# not
import config

# evernote
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import evernote.edam.type.ttypes as Types

#client = EvernoteClient(token=config.TOKEN, sandbox=False)

class NotClient(EvernoteClient):
    def __init__(self, *args, **kwargs):
        super(NotClient, self).__init__(*args, **kwargs)
        self.note_store = self.get_note_store()

    def get_content(self, note_guid):
        note = self.note_store.getNote(note_guid, True, False, False, False)
        return note.content

    def search(self, title):
        try:
            # evernote's api is ridiculous
            filter = NoteFilter(words="intitle:'{0}'".format(title))
            finder = self.note_store.findNotesMetadata(filter, 0, 1, NotesMetadataResultSpec())
            self.note_guid = finder.notes[0].guid
            return self.note_guid
        except:
            return False

    def save(self, body, title):
        '''
        if the note exists, update it
        else, create it
        '''
        if self.search(title):
            note = self.note_store.getNote(self.note_guid, True, False, False, False)
            save_it = self.note_store.updateNote
        else:
            note = Types.Note()
            save_it = self.note_store.createNote
        
        # evernotes special markup:
        note.title = title
        note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>{0}</en-note>'.format(body)

        # save new note or update existing
        save_it(note)
