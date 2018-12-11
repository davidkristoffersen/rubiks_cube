#!/usr/bin/env python3.7

from . import *
from traceback import format_exc
import re

if __name__ == '__main__':
    try:
        cube = Cube(input("Size of cube: "), time=0.05, do_print = True)
        while 1:
            err = cube.input(ask_inp = True)
            if err and not isinstance(err, list):
                print(err)
                input()

    except Exception as e:
        print(format_exc())
