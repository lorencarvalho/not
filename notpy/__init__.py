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

client = EvernoteClient(token=config.DEVTOKEN)

class Notary(object):
    def __init__(self, authtoken):
        self.authtoken = authtoken
        self.store = client.get_note_store()
        self.notefilter = NoteStore.NoteFilter()

    def get_content(self, note_guid):
        note = self.store.getNote(note_guid, True, False, False, False)
        return note.content
        

    def search(self, title):
        try:
            # evernote's api is ridiculous
            self.notefilter.words = 'intitle:"{0}"'.format(title)
            notes_metadata_result_spec = NoteStore.NotesMetadataResultSpec()
            notes_metadata_list = self.store.findNotesMetadata(self.notefilter, 0, 1, notes_metadata_result_spec)
            self.note_guid = notes_metadata_list.notes[0].guid
            # note = self.store.getNote(self.note_guid, True, False, False, False)
            return self.note_guid
        except:
            return False

    def save(self, body, title):
        if self.search(title):
            self.note = self.store.getNote(self.note_guid, True, False, False, False)
            save_it = self.store.updateNote
        else:
            self.note = Types.Note()
            save_it = self.store.createNote
        self.note.title = title
        self.note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        self.note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        self.note.content += '<en-note>{0}</en-note>'.format(body)
        save_it(self.note)
