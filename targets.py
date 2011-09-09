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


