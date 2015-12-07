# -*- coding: utf-8

import argparse

def main():
    parser = argparse.ArgumentParser(description='start')
    parser.add_argument('arg0', help="this is a argument.")
    parser.add_argument('square', help='test int', type=int)
    parser.add_argument('-v', '--version', help='select version')
    args = parser.parse_args()
    print args.arg0
    print args.square**2
    if args.version:
        print args.version
        print '*'*9

if __name__ == '__main__':
    main()