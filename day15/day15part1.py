#!/usr/bin/env python3

import sys
import re

import numpy as np

from collections import deque
from itertools import count

if len(sys.argv) > 1:
    input_filename = sys.argv[1]
else:
    dayn = re.match(r'.*day(\d+)\.py', sys.argv[0]).group(1)
    input_filename = 'inp' + dayn + '.txt'

GOB_AP = 3
class Unit:
    def __init__(self, type, pos, ap, hp=200):
        self.type = type
        self.pos = pos
        self.hp = hp
        self.alive = True
        self.ap = ap

    def take_turn(self):
        # move
        pass

lines = []
with open(input_filename) as f:
    for line in f:
        line = list(line)
        assert line.pop() == '\n'
        lines.append(line)

Y, X = len(lines), len(lines[0])
print(Y, X)
UNITS = []
grid = np.zeros((Y, X), dtype=np.int32)
INF = Y * X

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c in {'.', 'E', 'G'}:
            grid[y][x] = -1
            if c != '.':
                utype = 0 if c == 'E' else 1
                UNITS.append((utype, (y, x)))
        elif c == '#':
            grid[y][x] = INF
        else:
            raise ValueError(c)
del lines


def nei(y, x):
    nn = (y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)
    return ((ay, ax) for ay, ax in nn if ((0 <= ay < Y) and (0 <= ax < X)))

"""
-1  uninitialized
0   enemies
INF blocks
"""
def bsearch(spos, enemy):
    toproc = deque()
    smap = grid.copy()
    for upos, unit in units.items():
        if unit.type == enemy:
            smap[upos] = 0
        else:
            smap[upos] = INF
    for npos in nei(*spos):
        if smap[npos] == 0:
            return 1, npos
        elif smap[npos] == -1:
            toproc.append((1, npos, npos))  # dist, src_node, path_start
    while toproc:
        cdist, cpos, ppos = toproc.popleft()
        cdist += 1
        for npos in nei(*cpos):
            nval = smap[npos]
            if nval == INF:  # blocked
                continue
            if nval == 0:
                return cdist, ppos
            if smap[npos] == -1:# or cdist < smap[npos]:
                smap[npos] = cdist
                toproc.append((cdist, npos, ppos))
            else:
                assert cdist >= smap[npos]
    return INF, None


"""
# wall
. open
G goblin
E elf

- rounds of combat with alive units
- each unit take a turn = move + attack
- turns in reading order

Turn
- identify all possible targets
- no target = end
- identify adjacent open spots to target
- unit might already be in range
- not already in range && no open spot = no turn

not in range - move + attack
in range of target - only attack

move:
- don't if already in range of target
- consider current position of units
- consider targets that can be reached (no reach = no turn)
- cannot move into other units/walls
- multiple spots tied = reading order

attack:
- consider all targets in range(adjacent)
- no such target = no turn
- select target with fewest hit point (tie = reading order)
- deal damage = to attack power reducing hit points
- HP <= 0 -> target dies, spot becomes empty
- EG have 3 attack power & 200 HP

for round in count():
    for unit in sorted(units, key=pos):
        if unit.alive:
            unit.take_turn()
    rm_dead_units()
"""
def print_state():
    return
    if len(sys.argv) == 1:
        return
    T = ['E', 'G']
    for y, line in enumerate(grid):
        cl = []
        cs = []
        for x, c in enumerate(line):
            if grid[y][x] == INF:
                cl.append('#')
            elif (y, x) in units:
                cl.append(T[units[y, x].type])
                cs.append('{}({})'.format(T[units[y, x].type], units[y, x].hp))
            else:
                cl.append('.')
        print(''.join(cl) + '  ' + ''.join(cs))
    #input('Next?')
    print()


def check(elf_ap):
    global units
    units = {}
    cnt = [0, 0]
    for utype, upos in UNITS:
        uap = GOB_AP if utype == 1 else elf_ap
        units[upos] = Unit(utype, upos, uap)
        cnt[utype] += 1

    print_state()
    dead = []
    final = None
    for rnd in count(start=1):
        for unit in sorted(units.values(), key=lambda u: u.pos):
            if not unit.alive:
                continue
            if not all(cnt):
                final = rnd - 1
                break
            upos = unit.pos
            assert unit.alive
            enemy = 1 if unit.type == 0 else 0
            # move
            edist, nextpos = bsearch(upos, enemy)
            if edist == INF:  # no targets. dont move
                continue
            elif edist == 1:  # target is adjacent. only attack
                # find target with minimum HP
                attack = min((units[tpos] for tpos in nei(*upos)
                              if tpos in units and units[tpos].type == enemy),
                             key=lambda u: (u.hp, u.pos))
                attack.hp -= unit.ap
                if attack.hp <= 0:
                    attack.alive = False  # check HP
                    cnt[attack.type] -= 1
                    print("dead", rnd, attack.type, attack.pos)
                    dead.append(units.pop(attack.pos))
            else:  # target not adjacent, move first
                assert edist > 0
                unit.pos = nextpos  # could remove?
                assert nextpos not in units
                units[nextpos] = units.pop(upos)
                upos = nextpos
                # enemy dist reduces by 1
                if edist == 2:  # now in position to attack
                    attack = min((units[tpos] for tpos in nei(*upos)
                                  if tpos in units and units[tpos].type == enemy),
                                 key=lambda u: (u.hp, *u.pos))
                    attack.hp -= unit.ap
                    if attack.hp <= 0:
                        attack.alive = False  # check HP
                        cnt[attack.type] -= 1
                        print("dead", rnd, attack.type, attack.pos)
                        dead.append(units.pop(attack.pos))
        else:
            #print(rnd)
            print_state()
            if not all(cnt):
                final = rnd
        if final:
            print('partial', rnd)
            print_state()
            break

    return (final * sum(unit.hp for unit in units.values()))

for eap in count(start=4):
    res = check(eap)
    if res != 0:
        print('Minimum EAP', eap, 'Result',  res)
        break
