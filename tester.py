#!/usr/bin/env python3.7

from cube import *
from sys import argv
import re
from functools import reduce

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

def checker_board(cube):
    cube.input(['l2','r2','f2','b2','d2','u2'])

def benchmark(cube):
    for i in range(10000):
        cube.input('l')

def solve(cube):
    turns = []
    turns.append('l')

    cube.input(turns)

if __name__ == '__main__':
    args = parse_args()
    size = args['size']
    cube = Cube(size)

    solve(cube)
    # checker_board(cube)
    # benchmark(cube)
    cube.print_arr()
