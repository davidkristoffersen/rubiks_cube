#!/usr/bin/env python3.7

from common import *

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
