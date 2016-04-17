#!/usr/local/bin/python

if __name__ == '__main__':
    import argparse
    from launcher import StoreLauncher


    parser = argparse.ArgumentParser()
    parser.add_argument('criteria', nargs='?', help='Criteria to search for.')
    parser.add_argument('--all', '-a', action='store_true', help='Search all the webstores')
    parser.add_argument('--path', '-p', help='Set the path to the config file.')
    parser.add_argument('--store', '-s', help='Name a specific webstore.', default='bladehq')
    parser.add_argument('--list', '-l', action='store_true', help='List the webstores available for searching.')
    args = parser.parse_args()
    store_launcher = StoreLauncher(args.path)

    if args.list:
        store_launcher.header()
    import pdb; pdb.set_trace()
    if args.criteria and args.store:
        try:
            store_launcher.store_dispatch(args.criteria, args.store)
        except KeyError:
            store_launcher.header()
            print args.store, 'is not a valid webstore.'
    elif args.criteria and args.all:
        store_launcher.search(args.criteria)
