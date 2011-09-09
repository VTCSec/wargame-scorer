#!/usr/bin/env python2
import urllib2
from StringIO import StringIO

from services import http
from services import Service

def mock_response(req):
    if req.get_full_url() == "http://example.com":
        data = """
                <html>
            <body>
                <h1>Hello World!</h1>
                <owner>Dude</owner>
            </body>
            </html>"""

        resp = urllib2.addinfourl(StringIO(data), data, req.get_full_url())
        resp.code = 200
        resp.msg = "OK"
        return resp

class MyHTTPHandler(urllib2.HTTPHandler):
    def http_open(self, req):
        return mock_response(req)

my_opener = urllib2.build_opener(MyHTTPHandler)
urllib2.install_opener(my_opener)


def http_test():
    config = {'host':'http://example.com'}
    h = http.HttpService(config)
    assert h.verify_up()
    assert h.owner() == "Dude"

def services_test():
    assert 'http' in [p.name for p in Service.plugins]
