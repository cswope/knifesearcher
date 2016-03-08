#!/usr/local/bin/python

import argparse
from launcher import StoreLauncher

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('criteria', nargs='?', help='Search all the webstores.')
    parser.add_argument('--path', '-p', help='Set the path to the config file.', default='./knifesearcher/json/config.json')
    parser.add_argument('--store', '-s', help='Search only a specific webstore.', default='bladehq')
    parser.add_argument('--list', '-l', action='store_true', help='List the webstores available for searching.')
    args = parser.parse_args()

    while True:
        store_launcher = StoreLauncher(args.path)
        if args.list:
            store_launcher.header()
            break
        if args.store:
            try:
                store_launcher.store_dispatch(args.criteria, args.store)
            except KeyError:
                store_launcher.header()
                print args.store, 'is not a valid webstore.'
        else:
            store_launcher.search(args.criteria)
        break
