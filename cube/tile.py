#!/usr/bin/env python3.7

from .common import *

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

    def __eq__(self, other):
        if isinstance(other, str):
            return self.col == {'r': red, 'g': green, 'b': blue, 'y': yellow, 'w': white, 'o': orange}[other]
        else:
            return self.col == other.col

    def __str__(self):
        return self.col(self.char)

    def __repr__(self):
        return self.col(self.char)
