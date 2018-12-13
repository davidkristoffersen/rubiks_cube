#!/usr/bin/env python3.7

from . import *

from sys import argv
import re

def help():
    print('Usage: ./tester.py \d+|help')
    exit(0)

def parse_args():
    args = {'size': 3}
    if len(argv) > 1:
        if argv[1] == 'help':
            help()
        assert(re.match(r'^\d+$', argv[1]))
        args['size'] = int(argv[1])
    return args

if __name__ == '__main__':
    args = parse_args()
    size = args['size']
    ai = Cube_AI(size)

    # ai.scramble()
    # ai.solve()
    # ai.print_arr()
    ai.checker()
    print(ai)
