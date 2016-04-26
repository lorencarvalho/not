"""
this submodule provides not-setup and does
the oauth stuff for initial access to evernote
"""
from __future__ import print_function

import os

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from evernote.api.client import EvernoteClient

from .constants import CONSUMER_KEY, CONSUMER_SECRET


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """ serve the callback from evernote oauth """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("<html><head><title>Huzzah!</title></head>")
        self.wfile.write("<body><p>Successfully authorized with `not`</p>")
        self.wfile.close()

        # save the url path to a global to buble up past the http server
        global path
        path = self.path

    def log_message(self, format, *args):
        """ shutup logs """
        return


def parse_query_string(authorize_url):
    """ unpack the query string """
    uargs = authorize_url.split('?')
    vals = {}
    for pair in uargs[1].split('&'):
        key, value = pair.split('=', 1)
        vals[key] = value
    return vals


def single_serve():
    """ build the hacked up http server """
    return HTTPServer(('', 10668), Handler)


def setup():
    """
    oauth flow for new users or updating users
    adapted from https://gist.github.com/inkedmn/5041037
    """
    client = EvernoteClient(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        sandbox=False
    )

    request_token = client.get_request_token('http://localhost:10668')
    print(
        "Paste this URL in your browser and login:"
        "-> {url}  \n\n"
        "Be advised, this will save your oauth token in plaintext to ~/.not_token !"
        "if you aren't cool with that, ctrl-c now and never return!".format(
            url=client.get_authorize_url(request_token)
        )
    )
    single_server = single_serve()
    single_server.handle_request()
    auth_url = path  # noqa
    vals = parse_query_string(auth_url)
    auth_token = client.get_access_token(
        request_token['oauth_token'],
        request_token['oauth_token_secret'],
        vals['oauth_verifier']
    )
    with open(os.path.join(os.environ['HOME'], '.not_token'), 'w') as f:
        f.write(auth_token)
        print("Token saved.")
