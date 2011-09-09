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
import logging
import re

from . import Service

class HttpService(Service):

    name = 'http'

    def __init__(self, config):
        self.config = config

        if not 'host' in self.config:
            raise InvalidConfigException('HttpService: missing hostname')

        if not 'port' in self.config:
            self.config['port'] = 80

        if not 'text' in self.config:
            self.config['text'] = "Hello World"

        if not 'owner_regex' in self.config:
            self.config['owner_regex'] = "<owner>(.*)</owner>"

        self.contents = None

    def verify_up(self):
        try:
            f = urllib2.urlopen(self.config['host'])
            self.contents = f.read()
            return True
        except urllib2.HTTPError, e:
            logging.info("HttpService received HttpError: status %s" % (e.code))
            return False

        except urllib2.URLError, e:
            logging.info("HttpService received UrlError: %s" % (e))
            return False

    def owner(self):
        if self.contents is None:
            return None

        owner = re.findall(self.config['owner_regex'], self.contents)
        if len(owner) == 0:
            return None

        return owner[0]
