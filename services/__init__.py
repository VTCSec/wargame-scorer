#!/usr/bin/env python

import os
import glob

__all__ = [ os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/*.py")]


class InvalidConfigException(Exception):
    pass

class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)

    def get_plugin(cls, name):
        """Get an new plugin by name"""
        for p in cls.plugins:
            if p.name == name:
                return p
        return None


class Service:
    """
    The constructor is passed a dictionary containing the configuration
    options for the service.

    All Services must specify the 'name' attribute.
    """
    __metaclass__ = PluginMount

    def verify_up(self):
        """Returns a boolean representing whether the service is up or not"""
        pass

    def owner(self):
        """Returns a string containing the name of the owning team/player"""
        pass

