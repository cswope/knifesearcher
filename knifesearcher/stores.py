#!/usr/local/bin/python

from urlparse import urlparse, parse_qs, ParseResult
import json
import webbrowser


class Store(object):
    """Generate webstore search URLs with search criteria, and launch them in
    the systems default webbrowser.
    """

    find_key     = str  # POST request parameter key for search criteria
    criteria     = str  # search string
    url          = ParseResult  # the url in it's parsed state
    name         = str  # extracted from the domain in the url
    search_path  = str  # the path portion of the url
    cached_urls  = dict # urls that have been searched aleady

    def __init__(self, url=None, find_key=None):
        """Initiate a new Store.

        arg::url should be the url that the GO! (or submit, or whatever)
        button points to when you click on it for a webstore.

        Example:
        >>> # 'url' is the the URL captured from a webstore search.
        >>> # The "SEARCH" value in 'url' is arbitrary, it must be at least 1
        >>> # character long.
        >>> #
        >>> # 'find_key' tells the Store what value to replace in the url with
        >>> # search criteria
        >>> #
        >>> config = {
        >>>     "url": "http://www.cutleryshoppe.com/search.aspx?find=SEARCH",
        >>>     "find_key": "find"
        >>> }
        >>> s = Store(**config)
        >>> s.search('something')
        <<webbrowser.open_new_tab>(Store.url)>
        """
        self.find_key = find_key
        self.parse_url(url)
        assert self.find_key in self.search_params
        self.cached_urls = {}

    def __repr__(self):
        """Return a string represtation."""
        return '<stores.Store {}>'.format(self.name)

    def parse_url(self, url, criteria=None):
        """Set the url."""
        self.url           = urlparse(url)
        self.criteria      = criteria
        self.name          = self.url.netloc.split('.')[1]
        self.search_path   = self.url.path
        self.search_params = parse_qs(self.url.query)
        if self.criteria is not None:
            self.set_search_criteria(criteria)

    def set_search_criteria(self, criteria):
        """Add the search criteria to the search url."""
        self.search_params[self.find_key] = [criteria]
        key_value_pairs = map(
            lambda e: '='.join([e[0], e[1][0]]), self.search_params.items()
        )
        self.url = self.url._replace(query='&'.join(key_value_pairs))

    def search(self, criteria):
        """Perform the search."""
        if criteria not in self.cached_urls:
            self.set_search_criteria(criteria)
            self.cached_urls[criteria] = self.url.geturl()
        webbrowser.open_new_tab(self.cached_urls[criteria])
