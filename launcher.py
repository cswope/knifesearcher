#!/usr/local/bin/python

import json
import sys
import os

from stores import Store


class StoreLauncher(object):

    config    = list
    cached    = list
    webstores = list

    def __init__(self, path=None):
        if path is not None:
            self.configure(path)
        self.cached = []

    def configure(self, path=None):
        if os.path.exists(path) is False:
            msg = 'There\'s no config file at: {path}'.format(path=path)
            raise IOError(msg)
        with open(path, 'r') as f:
            self.config = json.loads(f.read())

    def set_webstores(self):
        self.webstores = [Store(**config) for config in self.config]

    def get_webstores(self):
        if self.webstores is list:
            self.set_webstores()
        return self.webstores

    def header(self):
        self.clear()
        print '-'*80
        print ', '.join([s.name for s in self.get_webstores()])
        print '-'*80

    @staticmethod
    def clear():
        sys.stderr.write("\x1b[2J\x1b[H")

    def search(self, criteria=None):
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
        dispatch = dict(map(lambda e: (e.name, e), self.get_webstores()))
        return dispatch[name].search(criteria)
