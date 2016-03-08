#!/usr/local/bin/python

from urlparse import urlparse, parse_qs, ParseResult
import json
import webbrowser


class Store(object):

    find_key     = str  # POST request parameter key for search criteria
    criteria     = str  # search string
    url          = ParseResult  # the url in it's parsed state
    name         = str  # extracted from the domain in the url
    search_path  = str
    cached_urls  = dict

    def __init__(self, url=None, find_key=None):
        self.find_key = find_key
        self.parse_url(url)
        assert self.find_key in self.search_params
        self.cached_urls = {}

    def __repr__(self):
        return '<stores.Store {}>'.format(self.name)

    def parse_url(self, url, criteria=None):
        self.url           = urlparse(url)
        self.criteria      = criteria
        self.name          = self.url.netloc.split('.')[1]
        self.search_path   = self.url.path
        self.search_params = parse_qs(self.url.query)
        if self.criteria is not None:
            self.set_search_criteria(criteria)

    def set_search_criteria(self, criteria):
        self.search_params[self.find_key] = [criteria]
        key_value_pairs = map(
            lambda e: '='.join([e[0], e[1][0]]), self.search_params.items()
        )
        self.url = self.url._replace(query='&'.join(key_value_pairs))

    def search(self, criteria):
        if criteria not in self.cached_urls:
            self.set_search_criteria(criteria)
            self.cached_urls[criteria] = self.url.geturl()
        webbrowser.open_new_tab(self.cached_urls[criteria])

