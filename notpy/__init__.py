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

client = EvernoteClient(token=config.DEVTOKEN)


class Notary(object):
    def __init__(self, authtoken):
        self.authtoken = authtoken

    def makenote(self, body):
        self.store = client.get_note_store()
        self.note = Types.Note()
        self.note.title = str(date.today())
        self.note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        self.note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        self.note.content += '<en-note>{0}</en-note>'.format(body)
        self.store.createNote(self.note)
