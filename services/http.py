#!/usr/bin/env python2

import urllib2
import logging
import re

class HttpService(object):

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
