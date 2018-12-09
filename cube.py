#!/usr/bin/env python3.7

from traceback import format_exc
from functools import reduce
import random
from time import sleep
import re
import sys
import getpass
import subprocess

def input2(value="",end=""):
    sys.stdout.write(value)
    data = getpass.getpass("")
    sys.stdout.write(data)
    sys.stdout.write(end)
    return data

col_pre ='\x1b[38;2;'
col_post='\x1b[m'
red     = lambda x: col_pre + '240;0;0m' + x + col_post
green   = lambda x: col_pre + '0;255;0m' + x + col_post
blue    = lambda x: col_pre + '30;144;255m' + x + col_post
yellow  = lambda x: col_pre + '255;255;0m' + x + col_post
orange  = lambda x: col_pre + '255;165;0m' + x + col_post
white   = lambda x: col_pre + '255;255;255m' + x + col_post
cols = [red, green, blue, yellow, orange, white]

def rand_col():
    return random.choice(cols)

def print_colors():
    print(red('red'), green('green'), blue('blue'), yellow('yellow'), orange('orange'), white('white'))

col_t = lambda col, opposite: {red: orange, orange: red, green: blue, blue: green, yellow: white, white: yellow}[col] if not opposite else col

class Cube(dict):
    def __init__(self, order):
        self.order = order
        self.create()
        self.undo_rotate_log = []
        self.undo_turn_log = []
        # self.turns = [['f', 'b', 'u', 'd', 'r', 'l', 'x', 'y', 'z'], ['', '2'], ['', '`']]
        self.turns = [['f', 'b', 'u', 'd', 'r', 'l'], ['', '2'], ['', '`']]

    def create(self):
        face_maps = {'f': red, 'r': green, 'l': blue, 'u': yellow, 'b': orange, 'd': white}
        faces = [Face(self.order, face_type, col) for face_type, col in face_maps.items()]
        o_dict = {face.type: face for face in faces}
        super().__init__(o_dict)

    def scramble(self, num_turns = 100, time = 1):
        for i in range(num_turns):
            bash('clear')
            print('Scrambling')
            print(cube)
            turn = self.random_turn()
            print(turn)
            self.turn(turn)
            sleep(time)
        bash('clear')
        print(cube)

    def solve(self, time = 1):
        while self.undo_turn_log:
            bash('clear')
            print('Solving')
            print(cube)
            turn = self.undo_turn_log.pop()
            print(turn)
            self.turn(turn, log_undo = False)
            sleep(time)
        bash('clear')
        print(cube)

    def random_turn(self):
        return random.choice(self.turns[0]) + random.choice(self.turns[1]) + random.choice(self.turns[2])

    def turn(self, sides, log_undo = True):
        if not isinstance(sides, list):
            sides = [sides]

        rotation = '+'
        for side in sides:
            if log_undo:
                undo_turn = side[:-1] if side[-1] == '`' else side + '`'
                self.undo_turn_log.append(undo_turn)

            if '`' in side:
                rotation = '-'
            double = 2 if '2' in side else 1
            side = side[0]
            for i in range(double):
                self.rotate_cube(side, rotation)

                if side in ['x', 'y', 'z']:
                    continue

                u = self['u'].side('d')
                r = self['r'].side('l')
                d = self['d'].side('u')
                l = self['l'].side('r')
                f = self['f']

                for i in range(self.order):
                    self.rotate([u[i], r[i], d[(i + 1) * -1], l[(i + 1) * -1]], rotation)
                self.rotate_face('f', rotation)
                self.undo_rotation()

    def rotate(self, org_tiles, direction):
        tiles = org_tiles if direction == '-' else org_tiles[::-1]
        for it, a in enumerate(tiles):
            if it == len(tiles) - 1:
                break
            tiles[it+1].col, a.col = a.col, tiles[it+1].col

    def rotate_face(self, face, direction):
        corners_by_level = lambda face, l: list(zip(face[l][l:-1 * (l + 1)], [y[-1 * (l + 1)] for y in face][l:-1 * (l +1)], face[-1 * (l + 1)][:l:-1][l:], [y[l] for y in face][:l:-1][l:]))

        face = self[face]
        for level in range(self.order // 2):
            for quad in corners_by_level(face, level):
                self.rotate(quad, direction)

    def __repr__(self):
        ret = ''
        ret += self.top('u')
        ret += '\n'
        ret += self.mid(['l', 'f', 'r', 'b'])
        ret += '\n'
        ret += self.bottom('d')
        return ret + '\n'

    def face_print(self, face):
        self.rotate_cube(face)

        u = 2 * ' ' + self['u'].side_to_str('d')
        d = 2 * ' ' + self['d'].side_to_str('u')
        r = self['r'].side_to_str('l')
        l = self['l'].side_to_str('r')
        f = str(self['f'])
        mid = self.f_zip(self.f_zip(l, f), r)

        print(u)
        print(mid)
        print(d)

        self.undo_rotation()

    def face_print_full(self, face):
        self.rotate_cube(face)

        print(self.top('u'))
        print(self.mid(['l', 'f', 'r']))
        print(self.bottom('d'))

        self.undo_rotation()

    def relative_face(self, org_face, face_type):
        if org_face == 'f':
            return {'f': 'f', 'b': 'b', 'u': 'u', 'd': 'd', 'r': 'r', 'l': 'l'}[face_type]
        elif org_face == 'b':
            return {'f': 'b', 'b': 'f', 'u': 'u', 'd': 'd', 'r': 'l', 'l': 'r'}[face_type]
        elif org_face == 'u':
            return {'f': 'u', 'b': 'd', 'u': 'b', 'd': 'f', 'r': 'r', 'l': 'l'}[face_type]
        elif org_face == 'd':
            return {'f': 'd', 'b': 'u', 'u': 'f', 'd': 'b', 'r': 'r', 'l': 'l'}[face_type]
        elif org_face == 'r':
            return {'f': 'r', 'b': 'l', 'u': 'u', 'd': 'd', 'r': 'b', 'l': 'f'}[face_type]
        elif org_face == 'l':
            return {'f': 'l', 'b': 'r', 'u': 'u', 'd': 'd', 'r': 'f', 'l': 'b'}[face_type]

    def relative_rotation(self, face, direction = None):
        return {
            'f': ([None], None), 'b': (['y', 'y'], '+'), 'u': (['x'], '+'), 'd': (['x'], '-'), 'r': (['y'], '-'), 'l': (['y'], '+'),
            'x': (['x'], direction), 'y': (['y'], direction), 'z': (['z'], direction)
        }[face]

    def opposite_rotation(self, face, direction = None):
        return {
            'f': ([None], None), 'b': (['y', 'y'], '+'), 'u': (['x'], '-'), 'd': (['x'], '+'), 'r': (['y'], '+'), 'l': (['y'], '-'),
            'x': (['x'], direction), 'y': (['y'], direction), 'z': (['z'], direction)
        }[face]

    def rotate_cube(self, rotation, direction = None):
        if not rotation:
            return

        rotations = self.relative_rotation(rotation, direction)
        undo = self.opposite_rotation(rotation, direction)
        self.undo_rotate_log.append(undo)

        if not rotations[1]:
            return

        for axis in rotations[0]:
            direction = rotations[1]

            old = self.copy()
            schema = {
                'x': {
                    '+': [
                        {'f': 'u', 'b': 'd', 'u': 'b', 'd': 'f', 'r': 'r', 'l': 'l'}, 
                        {'r': '-', 'l': '+', 'u': '+2','b': '+2'}],
                    '-': [
                        {'f': 'd', 'b': 'u', 'u': 'f', 'd': 'b', 'r': 'r', 'l': 'l'},
                        {'r': '+', 'l': '-', 'b': '+2', 'd': '+2'}],
                },
                'y': {
                    '+': [{'f': 'l', 'b': 'r', 'u': 'u', 'd': 'd', 'r': 'f', 'l': 'b'}, {'u': '-', 'd': '+'}],
                    '-': [{'f': 'r', 'b': 'l', 'u': 'u', 'd': 'd', 'r': 'b', 'l': 'f'}, {'u': '+', 'd': '-'}],
                },
                'z': {
                    '+': [
                        {'f': 'f', 'b': 'b', 'u': 'r', 'd': 'l', 'r': 'd', 'l': 'u'},
                        {'f': '-', 'b': '+', 'r': '-', 'l': '-', 'u': '-', 'd': '-'}],
                    '-': [
                        {'f': 'f', 'b': 'b', 'u': 'l', 'd': 'r', 'r': 'u', 'l': 'd'},
                        {'f': '+', 'b': '-', 'r': '+', 'l': '+', 'u': '+', 'd': '+'}],
                }
            }
            for k, v in schema[axis][direction][0].items():
                self[k] = old[v]
            for k, v in schema[axis][direction][1].items():
                if len(v) > 1:
                    self.rotate_face(k, v)
                self.rotate_face(k, v)

    def undo_rotation(self):
        if not self.undo_rotate_log:
            return
        undo = self.undo_rotate_log.pop()
        for axis in undo[0]:
            self.rotate_cube(axis, undo[1])

    def top(self, face):
        stred = self.f_str()
        return '\n'.join([self.order * 2 * ' ' + x for x in stred[face].split('\n')])

    def mid(self, faces):
        stred = self.f_str()
        faces[0] = stred[faces[0]]
        return reduce(lambda a, b: self.f_zip(a, stred[b]), faces)

    def bottom(self, face):
        stred = self.f_str()
        return '\n'.join([self.order * 2 * ' ' + x for x in stred[face].split('\n')])

    def f_str(self):
        return {type: str(face) for type, face in self.items()}

    def f_zip(self, a, b): 
        return '\n'.join([' '.join([str(y) for y in x]) for x in list(zip(a.split('\n'), b.split('\n')))])


class Face(list):
    def __init__(self, order, type, col):
        self.order = order
        self.type = type
        self.col = col
        self.create()

    def create(self):
        o_list = [[Tile('x', self.col) for y in range(self.order)] for x in range(self.order)]
        super().__init__(o_list)

    def __repr__(self):
        ret = ''
        for y in self:
            for x in y:
                ret += str(x) + ' '
            ret = ret[:-1] + '\n'
        return ret[:-1]

    def side(self, s):
        if s == 'l':
            return [tiles[0] for tiles in self]
        elif s == 'r':
            return [tiles[-1] for tiles in self]
        elif s == 'u':
            return [tile for tile in self[0]]
        elif s == 'd':
            return [tile for tile in self[-1]]

    def side_to_str(self, s):
        tiles = self.side(s)
        if s in ['l', 'r']:
            return '\n'.join([str(tile) for tile in tiles])
        elif s in ['u', 'd']:
            return ' '.join([str(tile) for tile in tiles])

class Tile():
    def __init__(self, char, col):
        self.col = col
        self.char = char

    def __add__(self, char):
        new = Tile(self.char, self.col)
        new.char += char
        return new

    def __mul__(self, mul):
        new = Tile(self.char, self.col)
        new.char *= mul
        return new

    def __str__(self):
        return self.col(self.char)

def bash(cmd):
    subprocess.run(cmd)
    # p = subprocess.Popen([cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # return tuple([e.decode('utf-8').rstrip() for e in t] for t in [x.readlines() for x in [p.stdout, p.stderr]])

if __name__ == '__main__':
    try:
        cube = Cube(3)
        while(1):
            bash('clear')
            print(cube)
            print('Turn: ', end='')
            inp_raw = input()
            for inp in [y for x in inp_raw.split(',') for y in x.split(' ')]:
                if inp in ['q', 'quit', '^C']:
                    exit(0)
                if not inp:
                    continue
                if inp == 'solve' or inp == 'sol':
                    cube.solve(time = 0.05)
                    continue
                if inp == 'turns' or inp == 'tur':
                    print(cube.undo_turn_log)
                    input()
                    continue
                if inp == 'new':
                    print('Cube size: ', end='')
                    inp = input()
                    cube = Cube(int(inp))
                if inp == 'scramble' or inp == 'scr':
                    cube.scramble(100, time = 0.05)
                    continue

                inp = ''.join(list(map(lambda x: "`" if x == "'" else x, inp)))
                if not re.match(r'^(f|b|u|d|r|l|x|y|z)$', inp[0]):
                    continue
                if len(inp) > 1 and not re.match(r'^2?`?$', inp[1:]):
                    continue
                cube.turn(inp)

    except Exception as e:
        print(format_exc())
