#!/usr/bin/env python

import config
import os
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from evernote.api.client import EvernoteClient


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write("<html><head><title>Huzzah!</title></head>")
        self.wfile.write("<body><p>Success!</p>")
        self.wfile.close()
        global path
        path = self.path


def parse_query_string(authorize_url):
    uargs = authorize_url.split('?')
    vals = {}
    for pair in uargs[1].split('&'):
        key, value = pair.split('=', 1)
        vals[key] = value
    return vals


def serve_one_request(server_class=HTTPServer, handler_class=Handler):
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
                consumer_key = config.CONSUMER_KEY,
                consumer_secret = config.CONSUMER_SECRET,
                sandbox = False
            )
    request_token = client.get_request_token('http://localhost:10668')
    print "Paste this URL in your browser and login"
    print client.get_authorize_url(request_token)
    print "Paste the URL you get after logging in here:"
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
        client = EvernoteClient(token=auth_token, sandbox=False)
        client.get_note_store()
