#!/usr/local/bin/python

import json
import sys
import os

from stores import Store


class StoreLauncher(object):
    """A configureable object that launches webstores."""

    config    = list
    cached    = list
    webstores = list

    def __init__(self, path=None):
        """Initiate a new instance of StoreLauncher."""
        if path is not None:
            self.configure(path)
        self.cached = []

    def configure(self, path=None):
        """Configure the StoreLauncher from a json compliant text file."""
        if os.path.exists(path) is False:
            msg = 'There\'s no config file at: {path}'.format(path=path)
            raise IOError(msg)
        with open(path, 'r') as f:
            self.config = json.loads(f.read())

    def set_webstores(self):
        """Generate the list of Store objects from the config."""
        self.webstores = [Store(**config) for config in self.config]

    def get_webstores(self):
        """Return the list of Store objects. Generate them and return them,
        if necessary.
        """
        if self.webstores is list:
            self.set_webstores()
        return self.webstores

    def header(self):
        """Print a nice fresh header."""
        self.clear()
        print '-'*80
        print ', '.join([s.name for s in self.get_webstores()])
        print '-'*80

    @staticmethod
    def clear():
        """A kind of hacky way of clearing the bash display. Stackoverflow,
        Always coming through.
        """
        sys.stderr.write("\x1b[2J\x1b[H")

    def search(self, criteria=None):
        """Execute searches for all stores.

        This will open a new tab for each webstore in the systems default
        browser, while the console prompts for the next search criteria.

        Each subsequent search will open more tabs for each webstore.
        """
        if criteria is None:
            criteria = raw_input('Enter search criteria: ')
            if criteria == '':
                return
        self.header()
        self.cached.append(criteria)
        for store in self.webstores:
            store.search(criteria)
        self.search()

    def store_dispatch(self, criteria, name):
        """Search a single Store."""
        dispatch = dict(map(lambda e: (e.name, e), self.get_webstores()))
        return dispatch[name].search(criteria)
