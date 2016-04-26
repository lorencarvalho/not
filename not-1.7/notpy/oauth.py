#!/usr/bin/env python
'''
this module provides not-setup and does
the oauth stuff for initial access to evernote
'''
import os
from config import CONSUMER_KEY, CONSUMER_SECRET
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from evernote.api.client import EvernoteClient


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''
        serve the callback from evernote oauth
        '''
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write("<html><head><title>Huzzah!</title></head>")
        self.wfile.write("<body><p>Successfully authorized with `not`</p>")
        self.wfile.close()
        global path
        path = self.path

    def log_message(self, format, *args):
        '''
        shutup logs
        '''
        return


def parse_query_string(authorize_url):
    '''
    unpack the query string
    '''
    uargs = authorize_url.split('?')
    vals = {}
    for pair in uargs[1].split('&'):
        key, value = pair.split('=', 1)
        vals[key] = value
    return vals


def serve_one_request(server_class=HTTPServer, handler_class=Handler):
    '''
    returns the subclassed http server
    '''
    server_address = ('', 10668)
    httpd = server_class(server_address, handler_class)
    return httpd


def setup():
    '''
    oauth flow for new users or updating users
    most of this was shamelessly copied from :
    https://gist.github.com/inkedmn/5041037
    '''
    client = EvernoteClient(
                consumer_key = CONSUMER_KEY,
                consumer_secret = CONSUMER_SECRET,
                sandbox = False
            )
    request_token = client.get_request_token('http://localhost:10668')
    print "Paste this URL in your browser and login:"
    print '  ', client.get_authorize_url(request_token)
    print '\n\n Be advised, this will save your oauth token in plaintext to ~/.not_token !'
    print 'if you aren\'t cool with that, ctrl-c now and never return!'
    serve_one_request().handle_request()
    authurl = path
    vals = parse_query_string(authurl)
    auth_token = client.get_access_token(
                 request_token['oauth_token'],
                 request_token['oauth_token_secret'],
                 vals['oauth_verifier']
                )
    with open(os.path.join(os.environ['HOME'], '.not_token'), 'w') as f:
        f.write(auth_token)
        print "Token saved."
