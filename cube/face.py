#!/usr/bin/env python3.7

from .tile import Tile
from .common import *

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

    def side(self, s, level):
        level = int(level) - 1 if level else 0
        if s == 'l':
            return [tiles[level] for tiles in self]
        elif s == 'r':
            return [tiles[-1 * (level + 1)] for tiles in self]
        elif s == 'u':
            return [tile for tile in self[level]]
        elif s == 'd':
            return [tile for tile in self[-1 * (level + 1)]]

    def side_to_str(self, s, level):
        tiles = self.side(s, level)
        if s in ['l', 'r']:
            return '\n'.join([str(tile) for tile in tiles])
        elif s in ['u', 'd']:
            return ' '.join([str(tile) for tile in tiles])
