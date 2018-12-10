#!/usr/bin/env python3.7

from cube import *
from sys import argv
import re

def parse_args():
    args = {'size': 3}
    if len(argv) > 1:
        assert(re.match(r'^\d+$', argv[1]))
        args['size'] = int(argv[1])
    return args

if __name__ == '__main__':
    args = parse_args()
    size = args['size']

    cube = Cube(size)
    print(cube)
    cube.input()
    print(cube)
