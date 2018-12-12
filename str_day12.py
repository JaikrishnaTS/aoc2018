#!/usr/bin/env python3

import sys
import re


test_inp = len(sys.argv) > 1 and sys.argv[1] == '-t'
dayn = re.match(r'.*day(\d+)\.py', sys.argv[0]).group(1)
input_filename = 'inp' + dayn + ('_' if test_inp else '') + '.txt'

nextg = {}

with open(input_filename) as f:
    init_str = 'initial state: '
    initial = f.readline().strip()
    assert initial.startswith(init_str)
    initial = initial[len(init_str):]
    f.readline()  # pass empty line
    for line in f:
        prevs, _, nexts = line.strip().partition(' => ')
        nextg[prevs] = nexts

prev = list(initial)
fi = 0

seen = {}
G = 50000000000
#G = 20

for i in range(G):
    prevs = ''.join(prev)
    if prevs in seen:
        print('{} seen before at {}'.format(i, seen[prevs]))
        break
    seen[prevs] = i
    firstp = prev.index('#')
    fi += (firstp - 2)
    if firstp > 4:
        prev = prev[firstp - 4:]
    elif firstp < 4:
        prev = ['.'] * (4 - firstp) + prev
    assert prev[:5] == ['.', '.', '.', '.', '#']
    while prev[-1] != '#':
        prev.pop()
    prev.extend(['.', '.', '.', '.'])
    assert prev[-5:] == ['#', '.', '.', '.', '.']
    curr = []
    for i in range(len(prev) - 4):
        curr.append(nextg[''.join(prev[i: i + 5])])
        #curr.append(nextg.get(''.join(prev[i: i + 5]), '.'))
    prev = curr

diff_gen = G - seen[''.join(prev)] - 1
firstp = prev.index('#')
fi += (firstp - 2) * diff_gen

print(sum((fi + i) for i in range(len(curr)) if curr[i] == '#'))

