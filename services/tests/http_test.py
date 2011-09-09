#!/usr/bin/env python2
# Copyright (c) 2011, Casey Link <unnamedrambler@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the organization nor the
#      names of its contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Casey Link BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
