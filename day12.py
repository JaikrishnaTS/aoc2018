#!/usr/bin/env python3

import sys
import re
from math import log2


test_inp = len(sys.argv) > 1 and sys.argv[1] == '-t'
dayn = re.match(r'.*day(\d+)\.py', sys.argv[0]).group(1)
input_filename = 'inp' + dayn + ('_' if test_inp else '') + '.txt'

def plant_mask(plantstr):
    ret = 0
    for x in plantstr:
        ret <<= 1
        if x == '#':
            ret |= 1
    return ret

nextg = [None] * (2 ** 5)

with open(input_filename) as f:
    init_str = 'initial state: '
    initial = f.readline().strip()
    assert initial.startswith(init_str)
    initial = initial[len(init_str):]
    f.readline()  # pass empty line
    for line in f:
        prevs, _, nexts = line.strip().partition(' => ')
        nextg[plant_mask(prevs)] = 1 if nexts == '#' else 0

M = 0b11111
prev = plant_mask(initial)
fi = 0
seen = {}

G = 50000000000
#G = 20

for i in range(G):
    if prev in seen:
        print('{} seen previously on {}'.format(i, seen[prev]))
        break
    seen[prev] = i
    fsb = int(log2(prev & (-prev)))
    if fsb < 4:
        prev <<= 4 - fsb
    elif fsb > 4:
        prev >>= fsb - 4
    #assert prev & M == 0b10000
    curr = 0
    for j in range(prev.bit_length() - 1, -1, -1):
        curr <<= 1
        curr |= nextg[(prev >> j) & M]
    ld = prev.bit_length() - curr.bit_length() - 2
    fi += ld
    prev = curr

diff_gen = G - seen[prev] - 1
fi += ld * diff_gen

currb = bin(curr)[2:]
#print(currb)
print(sum((fi + i) for i in range(len(currb)) if currb[i] == '1'))

