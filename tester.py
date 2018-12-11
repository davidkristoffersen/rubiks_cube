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

def rotate_face_to_face(cube, face_org, face_dest):
    rotate = {
        'f': {'r': 'y-','l': 'y', 'u': 'x', 'd': 'x-','b': 'y2','f': ''},
        'b': {'r': 'y', 'l': 'y-','u': 'x-','d': 'x', 'b': '',  'f': 'y2'},
        'u': {'r': 'z', 'l': 'z-','u': '',  'd': 'z2','b': 'x', 'f': 'x-'},
        'd': {'r': 'z-','l': 'z', 'u': 'z2','d': '',  'b': 'x-','f': 'x'},
        'r': {'r': '',  'l': 'y2','u': 'z-','d': 'z', 'b': 'z-','f': 'z'},
        'l': {'r': 'y2','l': '',  'u': 'z', 'd': 'z-','b': 'z', 'f': 'z-'}
    }[face_dest][face_org]
    cube.input(rotate)
    if rotate in ['z', 'z-', 'z2']:
        return {'z': -1, 'z-': 1, 'z2': 2}[rotate]
    return 0


def get_face_by_col(cube, col):
    for face in ['r', 'l', 'u', 'd', 'b', 'f']:
        if center_col(cube, face) == col:
            return face

def solve(cube):
    front_col = 'w'
    def cross():
        def edge(color):
            for face_id, face in cube.items():
                rotate_to_face_id(cube, face_id)
                # print()
                # print("\x1b[1mFace:", face_id, "\x1b[m")
                # print(cube)
                edges = [(0, 1), (1, 2), (2, 1), (1, 0)]
                for it, (y, x) in enumerate(edges):
                    bro = edge_brother(y, x)
                    this = face[y][x]
                    # print(bro)
                    if (this == color and bro == 'w'):
                        front_face = get_face_by_col(cube, front_col)
                        print('front_face:', front_face)
                        print('before rotate_face_to_face:\n',cube)
                        face_rot = rotate_face_to_face(cube, front_face, 'u')
                        print('after\n', cube)
                        print('face_rot:', face_rot, 'y, x', y, x)
                        y, x = edges[(it + face_rot) % 4]
                        print('y,x', y, x)
                        face_id = get_face_by_col(cube, face[1][1])
                        print('face_id', face_id)
                        bro = edge_brother(y, x)
                        this = cube[face_id][y][x]
                        side = {(0, 1): 'u', (1, 2): 'r', (2, 1): 'd', (1, 0): 'l'}[(y,x)]
                        if face_id in ['u', 'd']:
                            if face_id == 'u':
                                cube.input({'u': ['b', 'l-', 'd', 'l'], 'd': ['f', 'r-', 'f-', 'd-'], 
                                            'r': ['r', 'b-', 'd2', 'b'], 'l': ['l-', 'b', 'd2', 'b-']}[side])
                            else:
                                cube.input({'u': '', 'd': 'd2', 'r': 'd-', 'l': 'd'}[side])
                            color_face = get_face_by_col(cube, color)
                            first_turn = {'f': [''], 'r': ['d', 'y'], 'b': ['d2', 'y2'], 'l': ['d-', 'y-']}[color_face]
                            cube.input(first_turn + ['f2'])
                        else:
                            pass
                        # print("Matches!", this, bro)
                        # print(cube)
                rotate_to_color(cube, front_col)
            print()

        def edge_brother(y, x):
            direction = {(0, 1): 'u', (1, 0): 'l', (1, 2): 'r', (2, 1): 'd'}[(y,x)]
            newy, newx = {(0, 1): (2, 1), (1, 0): (1, 2), (1, 2): (1, 0), (2, 1): (0, 1)}[(y, x)]
            tile = cube[direction][newy][newx]
            return tile

        rotate_to_color(cube, front_col)
        print(cube)
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
