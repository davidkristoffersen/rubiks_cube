#!/usr/bin/env python3.7

from . import *
from traceback import format_exc
import re

if __name__ == '__main__':
    try:
        cube = Cube(input("Size of cube: "))
        while 1:
            err = cube.input()
            if err:
                print(err)
                input()

    except Exception as e:
        print(format_exc())
