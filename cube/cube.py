#!/usr/bin/env python3.7

from .face import Face
from .tile import Tile
from .common import *

from functools import reduce
import random
from time import sleep
from copy import deepcopy

class Cube(dict):
    def __init__(self, order, time = 1, do_print = False):
        assert(re.match(r'^\d+$', str(order)))
        self.order = int(order)
        self.create()
        self.undo_rotate_log = []
        self.undo_turn_log = []
        self.turns = [['f', 'b', 'u', 'd', 'r', 'l', 'm', 'e', 's'], ['', '2'], ['', '-']]
        self.time = time
        self.do_print = do_print

    def create(self):
        face_maps = {'f': red, 'r': green, 'l': blue, 'u': yellow, 'b': orange, 'd': white}
        faces = [Face(self.order, face_type, col) for face_type, col in face_maps.items()]
        o_dict = {face.type: face for face in faces}
        super().__init__(o_dict)

    def scramble(self, num_turns = 100):
        for i in range(num_turns):
            if self.do_print:
                bash('clear')
                print('Scrambling')
                print(self)
            turn = self.random_turn()
            while not turn:
                turn = self.random_turn()
            for i in range(turn['double']):
                self.turn(turn['face'], turn['direction'], turn['inner'], turn['together'])
            if self.do_print:
                sleep(self.time)
        if self.do_print:
            bash('clear')
            print(self)

    def solve(self):
        while self.undo_turn_log:
            if self.do_print:
                bash('clear')
                print('Solving')
                print(self)
            turn = self.undo_turn_log.pop()
            turn = input_to_turn(turn, self.order)
            for i in range(turn['double']):
                self.turn(turn['face'], turn['direction'], turn['inner'], turn['together'], log_undo = False)
            if self.do_print:
                sleep(self.time)
        if self.do_print:
            bash('clear')
            print(self)

    def random_turn(self):
        inner = '' if self.order < 4 else str(random.choice(['', random.randint(2, self.order // 2)]))
        together = '' if not inner else random.choice(['', 'w'])
        face = random.choice(self.turns[0])
        direction = random.choice(self.turns[2])
        double = random.choice(self.turns[1])
        inp = inner + face + together + double + direction
        return input_to_turn(inp, self.order)

    def turn_s(self, undo, direction, together):
        self.turn('x', '+', '', '', log_undo = undo)
        self.turn('d', direction, str((self.order // 2) + 1), together, log_undo = undo)
        self.turn('x', '-', '', '', log_undo = undo)

    def turn_w(self, face, direction, inner, undo):
        inner = 1 if not inner else int(inner)
        for inner in range(1, inner + 1):
            if inner == 1:
                inner = ''
            self.turn(face, direction, str(inner), '', log_undo = undo)

    def turn(self, face, direction, inner, together, log_undo = True):
        if face == 's':
            self.turn_s(log_undo, direction, together)
            return
        if together == 'w':
            self.turn_w(face, direction, inner, log_undo)
            return

        if log_undo:
            undo_turn = inner + face
            undo_turn += '-' if direction == '+' else ''
            self.undo_turn_log.append(undo_turn)

        self.rotate_cube(face, direction)

        if face in ['x', 'y', 'z']:
            return

        u = self['u'].side('d', inner)
        r = self['r'].side('l', inner)
        d = self['d'].side('u', inner)
        l = self['l'].side('r', inner)

        for i in range(self.order):
            self.rotate([u[i], r[i], d[(i + 1) * -1], l[(i + 1) * -1]], direction)
        if not inner:
            self.rotate_face('f', direction)

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

        u = 2 * ' ' + self['u'].side_to_str('d', '')
        d = 2 * ' ' + self['d'].side_to_str('u', '')
        r = self['r'].side_to_str('l', '')
        l = self['l'].side_to_str('r', '')
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
        return '\n'.join([(self.order * 2 + 2) * ' ' + x for x in stred[face].split('\n') + ['-' * (self.order * 2 - 1)]])

    def mid(self, faces):
        right_line = lambda face: '\n'.join([x + ' |' for x in face.split('\n')])
        stred = self.f_str()
        faces[0] = right_line(stred[faces[0]])
        faces[1] = right_line(stred[faces[1]])
        if len(faces) == 4:
            faces[2] = right_line(stred[faces[2]])
            faces[3] = stred[faces[3]]
        else:
            faces[2] = stred[faces[2]]
        return reduce(lambda a, b: self.f_zip(a, b), faces)

    def bottom(self, face):
        stred = self.f_str()
        return '\n'.join([(self.order * 2 + 2) * ' ' + x for x in ['-' * (self.order * 2 - 1)] + stred[face].split('\n')])

    def f_str(self):
        return {type: str(face) for type, face in self.items()}

    def f_zip(self, a, b): 
        return '\n'.join([' '.join([str(y) for y in x]) for x in list(zip(a.split('\n'), b.split('\n')))])

    def items(self):
        return [(k, self[k]) for k in ['f', 'l', 'u', 'r', 'd', 'b']]

    def to_3d_array(self):
        arr = []
        arr.append(deepcopy(self['f']))
        arr.append(deepcopy(self['l']))
        arr.append(deepcopy(self['u']))
        arr.append(deepcopy(self['r']))
        arr.append(deepcopy(self['d']))
        arr.append(deepcopy(self['b']))
        return arr

    def print_arr(self, arr = None):
        if not arr:
            arr = self.to_3d_array()
        ret = ''
        ret_arr = []
        for zt, z in enumerate(arr):
            ret = '\x1b[1m' + str(zt) + '\x1b[m ' + ' ' * len(arr[0]) + '\n'
            ret += '├─' + ''.join([str(x) for x in range(len(arr[0]))])
            for yt, y in enumerate(z):
                ret += '\n' + str(yt) + ' '
                for xt, x in enumerate(y):
                    ret += str(x)
            ret_arr.append(ret)
        new = reduce(lambda a, b: self.f_zip(a, b), ret_arr)
        print(new)

    def input(self, inp_raw='', ask_inp = False):
        if isinstance(inp_raw, list):
            inp_raw = ','.join(inp_raw)
        if not inp_raw and ask_inp:
            bash('clear')
            print(self)

            print('Turn: ', end='')
            inp_raw = input()

        err = ''
        for inp in [y for x in inp_raw.split(',') for y in x.split(' ') if y]:
            turn = input_to_turn(inp, self.order)
            if not turn and inp_raw not in ['q', 'quit', '^C', 'show', 'solve', 'sol', 'scramble', 'scr', 'turns', 'tur', 'new']:
                err = inp
                
        if err:
            return "Invalid input!\n" + "raw input: " + inp_raw + "\nInvalid part: " + err

        for inp in [y for x in inp_raw.split(',') for y in x.split(' ') if y]:
            if inp in ['q', 'quit', '^C']:
                exit(0)
            if not inp:
                continue
            if inp == 'show':
                print(self)
                continue
            if inp == 'solve' or inp == 'sol':
                self.solve()
                continue
            if inp == 'scramble' or inp == 'scr':
                self.scramble(200)
                continue
            if inp == 'turns' or inp == 'tur':
                print(self.undo_turn_log)
                input()
                continue

            turn = input_to_turn(inp, self.order)
            if not turn:
                continue
            for i in range(turn['double']):
                self.turn(turn['face'], turn['direction'], turn['inner'], turn['together'])
        # return self.to_3d_array()
