#!/usr/bin/env python

import config
from evernote.api.client import EvernoteClient

def parse_query_string(authorize_url):
    uargs = authorize_url.split('?')
    vals = {}
    if len(uargs) == 1:
        raise Exception('Invalid Authorization URL')
    for pair in uargs[1].split('&'):
        key, value = pair.split('=', 1)
        vals[key] = value
    return vals


def callback_http():
    import SimpleHTTPServer
    import SocketServer
    port = 10666
    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", port), handler)
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
    httpd = callback_http()
    request_token = client.get_request_token('http://localhost:10666')
    httpd.handle_request()
    print "Paste this URL in your browser and login"
    print client.get_authorize_url(request_token)
    print "Paste the URL you get after logging in here:"
    authurl = raw_input()
    vals = parse_query_string(authurl)
    auth_token = client.get_access_token(
                 request_token['oauth_token'],
                 request_token['oauth_token_secret'],
                 vals['oauth_verifier']
                )
    with open(os.path.join(os.environ.get['HOME'], '.not_token')) as f:
        f.write(auth_token)
