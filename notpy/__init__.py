#!/usr/bin/env python
'''
provides NotClient, the subclassed evernote client
'''
import re
import logging

# evernote imports
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from evernote.edam.type.ttypes import NoteSortOrder
import evernote.edam.type.ttypes as Types


class NoteSaveError(Exception):
    def __init__(self, original_exc, note_contents=''):
        '''
        return a cleanly formatted exception but also
        print the unsaved note to stdout
        '''
        message = "Exception message: {0}\nUnsaved note contents: {1}".format(original_exc, note_contents)
        super(NoteSaveError, self).__init__(message)


class NotClient(EvernoteClient):
    def __init__(self, *args, **kwargs):
        '''
        subclass evernote client and get a note store obj
        '''
        super(NotClient, self).__init__(*args, **kwargs)
        self.note_store = self.get_note_store()
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_content(self, note_guid):
        '''
        get the actual contents of a note based on guid
        '''
        note = self.note_store.getNote(note_guid, True, False, False, False)
        # Strip html/xml tags
        content = re.sub('<br/>', '\n', note.content)
        content = re.sub('<.*?>', '', content)
        self.logger.debug("Got text content from note guid {0}: {1}".format(note_guid, content))
        return content

    def get_title(self, note_guid):
        note = self.note_store.getNote(note_guid, True, False, False, False)
        return note.title

    def search(self, title=None, ls=False):
        '''
        bumble through evernote's api to find a note or ten
        what a terrible method... it either returns a guid or a list of guids
        '''
        if ls:
            notefilter = NoteFilter(order=NoteSortOrder.UPDATED)
            finder = self.note_store.findNotesMetadata(notefilter, 0, 10, NotesMetadataResultSpec())
            guids = [note.guid for note in finder.notes]
            return guids

        try:
            # evernote's api is ridiculous
            notefilter = NoteFilter(words="intitle:'{0}'".format(title))
            finder = self.note_store.findNotesMetadata(notefilter, 0, 1, NotesMetadataResultSpec())
            self.note_guid = finder.notes[0].guid  # what am i doing...
            return self.note_guid  # returning... the ... attribute?
        except:
            return False

    def check_tags(self, body):
        '''
        search the note for 'tags: tag1, tag2'
        '''
        for line in body.split('\n'):
            if line.startswith('tags:'):
                return line.split('tags:')[1].replace(' ', '').split(',')

    def save(self, body, title):
        '''
        if the note exists, update it
        else, create it
        '''
        try:
            if self.search(title):
                note = self.note_store.getNote(self.note_guid, True, False, False, False)
                save_it = self.note_store.updateNote
            else:
                note = Types.Note()
                save_it = self.note_store.createNote

            # look for and save tags:
            note.tagNames = self.check_tags(body)

            # evernotes special markup:
            note.title = title
            note.content = '<?xml version="1.0" encoding="UTF-8"?>'
            note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
            note.content += '<en-note>{0}</en-note>'.format(body)
            note.content = re.sub('\n', '<br/>', note.content)

            # save new note or update existing
            save_it(note)
        except Exception as e:
            raise NoteSaveError(e, body)
