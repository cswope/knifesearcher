#!/usr/local/bin/python

import unittest

from urlparse import ParseResult

from .. import stores


class TestBaseStore(unittest.TestCase):

    BS = stores.BaseStore
    assert hasattr(BS, 'name')
    assert hasattr(BS, 'url')
    assert hasattr(BS, 'search_path')
    assert hasattr(BS, 'search_params')

    def test_cutleryshoppe(self):
        parameters = {
            'name'         : 'cutleryshoppe',
            'url'          : 'http://www.cutleryshoppe.com',
            'search_path'  : 'search.aspx',
            'search_params': {'find': 'gfddfgdfg'}
        }





if __name__ == '__main__':
    unittest.main()
