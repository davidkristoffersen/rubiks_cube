#!/usr/bin/env python3.7

import random
import re
import subprocess

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

def bash(cmd):
    subprocess.run(cmd)
    # p = subprocess.Popen([cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # return tuple([e.decode('utf-8').rstrip() for e in t] for t in [x.readlines() for x in [p.stdout, p.stderr]])

def input_to_turn(inp, order):
    inner = ''
    import inspect
    if not re.match(r'^(f|b|u|d|r|l|x|y|z|m|e|s)$', inp[0]):
        inner = re.match(r'^\d+', inp)
        if inner:
            inner = inner.group()
            inner = inp[:len(inner)]
            inp = inp[len(inner):]
        else:
            return None
        if not inp or not re.match(r'^(f|b|u|d|r|l|x|y|z|m|e|s)$', inp[0]):
            return None

    face = inp[0]
    inp = inp[1:]

    if face in "mes":
        inner = str((order // 2) + 1)
        face = {'m': 'l', 'e': 'd', 's': 's'}[face]
    elif len(inner) and int(inner) > (order // 2) + 1: 
        return None

    together = re.match(r'^w', inp)
    if together:
        inp = inp[1:]
        together = 'w'
    else:
        together = ''

    inp = ''.join(list(map(lambda x: "-" if x in "'`-" else x, inp)))
    if len(inp) and not re.match(r'^2?-?$', inp):
        # print(inspect.getframeinfo(inspect.currentframe()).lineno)
        return None

    double = 2 if re.match(r'2', inp) else 1
    direction = '-' if len(inp) and re.match(re.escape("-"), inp[-1]) else '+'
    
    return {'face': face, 'direction': direction, 'inner': inner, 'double': double, 'together': together}
