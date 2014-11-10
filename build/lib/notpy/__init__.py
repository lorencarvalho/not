#!/usr/bin/env python

# stdlib
import os
import sys
import tempfile
from datetime import date
from subprocess import call

# not
import config

# evernote
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types

dev_token = "S=s1:U=8fd7d:E=150ee5deb6c:C=14996acbb98:P=1cd:A=en-devtoken:V=2:H=35f6824f584ba40a6b596167e0e9ca25"
client = EvernoteClient(token=dev_token)

def notary():
    
    store = client.get_note_store()
    note = Types.Note()
    note.title = date.today()

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tempfile:
        call([config.EDITOR, tempfile.name])
        note.content = open(tempfile.name).read()
        store.createNote(note)

    print "fin."
