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

def center_col(cube, face):
    return cube[face][1][1]

def rotate_to_face_id(cube, face):
    col = center_col(cube, face)
    rotate_to_color(cube, col)

def rotate_to_color(cube, col):
    for k, v in {'r': 'y-', 'l': 'y', 'u': 'x', 'd': 'x-', 'b': 'y2', 'f': ''}.items():
        if center_col(cube, k) == col:
            cube.input(v)
            break

def solve(cube):
    front_col = 'w'
    def cross():
        def edge(color):
            for face_id, face in cube.items():
                print(face_id)
                for y, x in [(0, 1), (1, 0), (1, 2), (2, 1)]:
                    bro = edge_brother(face_id, face, y, x)
                    this = face[y][x]
                    print(this, bro)
                    if (this == color and bro == 'w') or (this == 'w' and bro == color):
                        print(this, bro)
            print()

        def edge_brother(face_id, face, y, x):
            rotate_to_face_id(cube, face_id)
            direction = {(0, 1): 'x', (1, 0): 'y', (1, 2): 'y-', (2, 1): 'x-'}[(y,x)]
            cube.input(direction)
            newy, newx = {(0, 1): (2, 1), (1, 0): (1, 2), (1, 2): (1, 0), (2, 1): (0, 1)}[(y, x)]
            tile = face[newy][newx]
            rotate_to_color(cube, front_col)
            return tile

        rotate_to_color(cube, front_col)
        edge('r')
    cross()

if __name__ == '__main__':
    args = parse_args()
    size = args['size']
    cube = Cube(size)

    # checker_board(cube)
    # benchmark(cube)

    cube.scramble()
    print(cube)
    solve(cube)
    cube.print_arr()
    print()
    print(cube)
