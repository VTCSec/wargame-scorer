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

"""
Functions for managing targets.
"""

import json
import logging
import os
import glob

import services
from services import *


class Target(object):
    def __init__(self, json_desc):
        config = json.loads(json_desc)
        self.name = config['name']
        self.host = config['host']

        self.services = []

        for service in config['services']:
            name = service['service']

            plugin = services.Service.get_plugin(name)
            if plugin is None:
                logging.warning("Failed to load service %s from %s target: Service not found" % (name, self.name))
                continue

            optional = service.get('optional', False)
            value = service['value']

            # parse the custom config for the plugin
            if name in config:
                service_config = config[name]
                service_config['host'] = self.host
            else:
                service_config = { 'host': self.host }

            logging.info("Plugin %s: loaded service %s" % (self.name, name))
            self.services.append( {'plugin': plugin, 'optional': optional, 'value': value, 'config': service_config } )

class CheckResponse(object):
    def __init__(self, target):
        self.target = target
        self.service_checks = {}

        for service in target.services:
            self.service_checks[service.plugin.name] = { 'up': False, 'owner': None }


def load_targets(dir = './targets'):
    """
    Loads all available targets from the targets/ directory
    """
    target_descs = [ os.path.basename(f) for f in glob.glob(dir+"/*.json") ]
    targets = []
    for desc in target_descs:
       json = open('%s/%s' % (dir, desc), 'r').read()
       targets.append(Target(json))
    return targets


